# logout destroys windows and opens login screen

from unittest.mock import MagicMock, patch

from tkinter import Tk, Toplevel


def test_dashboard_logout_calls_run_login(seeded_db, tmp_path):
    import os
    import sys
    _conftest_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _conftest_dir not in sys.path:
        sys.path.insert(0, _conftest_dir)
    from conftest import _MINIMAL_PNG

    img_dir = tmp_path / "images"
    img_dir.mkdir()
    for name in ("logo1.png", "menu_im.png", "side.png"):
        (img_dir / name).write_bytes(_MINIMAL_PNG)

    import dashboard
    dashboard.IMAGE_DIR = str(img_dir)

    root = Tk()
    root.withdraw()
    ims = dashboard.IMS(root)

    with patch("dashboard.run_login", new_callable=MagicMock) as mock_run_login:
        ims.logout()
        mock_run_login.assert_called_once()


def test_billing_logout_calls_run_login(billing_app):
    bill = billing_app
    with patch("login.run_login", new_callable=MagicMock) as mock_run_login:
        bill.logout()
        mock_run_login.assert_called_once()


def test_billing_logout_from_toplevel_destroys_parent_and_calls_run_login(billing_seeded_db, tmp_path):
    import sys
    import os
    _conftest_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    if _conftest_dir not in sys.path:
        sys.path.insert(0, _conftest_dir)
    from conftest import _MINIMAL_PNG

    img_dir = tmp_path / "images"
    img_dir.mkdir()
    (img_dir / "logo1.png").write_bytes(_MINIMAL_PNG)

    import billing
    billing.IMAGE_DIR = str(img_dir)

    root = Tk()
    root.withdraw()
    bill_win = Toplevel(root)
    bill = billing.billClass(bill_win)

    real_destroy = root.destroy
    parent_destroy = MagicMock()
    root.destroy = parent_destroy 

    with patch("login.run_login", new_callable=MagicMock) as mock_run_login:
        bill.logout()
        mock_run_login.assert_called_once()
        parent_destroy.assert_called_once()

    root.destroy = real_destroy
    root.destroy()
