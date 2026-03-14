# pytest fixtures

import base64
import os
import sys

import pytest

_MINIMAL_PNG = base64.b64decode(
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mNk+M9QDwADhgGAWjR9awAAAABJRU5ErkJggg=="
)

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)


@pytest.fixture(scope="function")
def test_db(tmp_path):
    db_path = tmp_path / "test_ims.db"
    os.environ["IMS_DB_PATH"] = str(db_path)
    yield str(db_path)
    if "IMS_DB_PATH" in os.environ:
        del os.environ["IMS_DB_PATH"]


@pytest.fixture
def seeded_db(test_db):
    from create_db import create_db
    from db_utils import execute_update

    create_db()
    execute_update(
        "INSERT INTO users(name,email,password) VALUES(?,?,?)",
        ("Test User", "test@example.com", "pass123"),
    )
    execute_update("INSERT INTO category(name) VALUES(?)", ("Electronics",))
    execute_update(
        "INSERT INTO product(Category,Supplier,name,price,qty,status) VALUES(?,?,?,?,?,?)",
        ("Electronics", "Supplier1", "Widget", "10.50", "100", "Active"),
    )
    return test_db


@pytest.fixture
def billing_seeded_db(test_db):
    from create_db import create_db
    from db_utils import execute_update

    create_db()
    execute_update("INSERT INTO category(name) VALUES(?)", ("Electronics",))
    execute_update(
        "INSERT INTO product(Category,Supplier,name,price,qty,status) VALUES(?,?,?,?,?,?)",
        ("Electronics", "Supplier1", "Widget", "10.50", "100", "Active"),
    )
    execute_update(
        "INSERT INTO product(Category,Supplier,name,price,qty,status) VALUES(?,?,?,?,?,?)",
        ("Electronics", "Supplier1", "Gadget", "5.00", "50", "Active"),
    )
    return test_db


@pytest.fixture
def billing_app(billing_seeded_db, tmp_path):
    img_dir = tmp_path / "images"
    img_dir.mkdir()
    (img_dir / "logo1.png").write_bytes(_MINIMAL_PNG)
    os.environ["IMS_IMAGE_DIR"] = str(img_dir)
    bill_dir = tmp_path / "bill"
    bill_dir.mkdir()
    try:
        import billing
        billing.IMAGE_DIR = str(img_dir)
        billing.BILL_DIR = str(bill_dir)
        from tkinter import Tk
        root = Tk()
        root.withdraw()
        bill = billing.billClass(root)
        yield bill
        try:
            root.destroy()
        except Exception:
            pass
    finally:
        if "IMS_IMAGE_DIR" in os.environ:
            del os.environ["IMS_IMAGE_DIR"]
