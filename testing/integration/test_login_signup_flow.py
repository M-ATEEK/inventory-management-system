# signup then login - uses actual SignupWindow.register and login DB query

from unittest.mock import patch

from db_utils import execute_fetchone
from signup import SignupWindow
from tkinter import Tk


def test_signup_then_login_success(test_db):
    from create_db import create_db
    create_db()

    root = Tk()
    root.withdraw()
    signup_win = SignupWindow(root, on_login_click=None)

    signup_win.var_name.set("New User")
    signup_win.var_email.set("newuser@test.com")
    signup_win.var_password.set("mypass")

    with patch.object(signup_win, "_go_to_login"): 
        with patch("signup.messagebox"):
            signup_win.register()

    row = execute_fetchone("SELECT * FROM users WHERE email=?", ("newuser@test.com",))
    assert row is not None
    assert row[1] == "New User"

    login_row = execute_fetchone(
        "SELECT * FROM users WHERE email=? AND password=?",
        ("newuser@test.com", "mypass"),
    )
    assert login_row is not None
    assert login_row[2] == "newuser@test.com"

    root.destroy()


def test_signup_duplicate_email_rejected(test_db):
    from create_db import create_db
    create_db()

    root = Tk()
    root.withdraw()
    signup_win = SignupWindow(root, on_login_click=None)

    signup_win.var_name.set("First User")
    signup_win.var_email.set("dup@test.com")
    signup_win.var_password.set("pass1")

    with patch.object(signup_win, "_go_to_login"):
        with patch("signup.messagebox") as mb:
            signup_win.register()

    assert execute_fetchone("SELECT * FROM users WHERE email=?", ("dup@test.com",)) is not None

    signup_win.var_name.set("Second User")
    signup_win.var_password.set("pass2")
    with patch.object(signup_win, "_go_to_login"):
        with patch("signup.messagebox") as mb:
            signup_win.register()
            mb.showerror.assert_called_once()
            assert "already registered" in mb.showerror.call_args[0][1].lower()

    rows = execute_fetchone("SELECT * FROM users WHERE email=?", ("dup@test.com",))
    assert rows is not None
    assert rows[1] == "First User"

    root.destroy()
