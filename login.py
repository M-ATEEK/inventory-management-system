from tkinter import *
from tkinter import messagebox

from db_utils import execute_fetchone, BASE_DIR
import os

IMAGE_DIR = os.path.join(BASE_DIR, "images")


def run_dashboard():
    from dashboard import IMS
    root = Tk()
    obj = IMS(root)
    root.mainloop()


def run_signup():
    from signup import SignupWindow
    root = Tk()
    obj = SignupWindow(root, on_login_click=run_login)
    root.mainloop()


def run_login():
    root = Tk()
    root.geometry("450x350+500+200")
    root.config(bg="white")
    root.resizable(False, False)
    root.title("Login")

    var_email = StringVar()
    var_password = StringVar()

    title = Label(root, text="Login", font=("goudy old style", 22, "bold"),
                  bg="#184a45", fg="white").pack(side=TOP, fill=X, pady=20)

    lbl_email = Label(root, text="Email", font=("goudy old style", 15), bg="white").place(x=50, y=100)
    Entry(root, textvariable=var_email, font=("goudy old style", 15), bg="lightyellow").place(x=180, y=100, width=220)

    lbl_password = Label(root, text="Password", font=("goudy old style", 15), bg="white").place(x=50, y=150)
    Entry(root, textvariable=var_password, font=("goudy old style", 15), bg="lightyellow", show="*").place(x=180, y=150, width=220)

    def do_login():
        email = var_email.get().strip()
        password = var_password.get()

        if not email:
            messagebox.showerror("Error", "Email is required", parent=root)
            return
        if not password:
            messagebox.showerror("Error", "Password is required", parent=root)
            return

        try:
            row = execute_fetchone("SELECT * FROM users WHERE email=? AND password=?", (email, password))
            if not row:
                messagebox.showerror("Error", "Invalid email or password", parent=root)
                return
            root.destroy()
            run_dashboard()
        except Exception as ex:
            messagebox.showerror("Error", f"Error: {ex}", parent=root)

    btn_login = Button(root, text="Login", command=do_login,
                      font=("Helvetica", 13, "bold"), bg="#2196f3", fg="white",
                      cursor="hand2", highlightthickness=0).place(x=180, y=210, width=120, height=35)

    def go_signup():
        root.destroy()
        run_signup()

    btn_signup = Button(root, text="Sign Up", command=go_signup,
                       font=("Helvetica", 12, "bold"), bg="#607d8b", fg="white",
                       cursor="hand2", highlightthickness=0).place(x=180, y=260, width=120, height=30)

    root.mainloop()


if __name__ == "__main__":
    from create_db import create_db
    create_db()
    run_login()
