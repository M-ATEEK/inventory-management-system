# billing flow - uses actual billClass, add_update_cart, generate_bill

from unittest.mock import patch

from db_utils import execute_fetchall, execute_fetchone


def test_billing_full_flow_updates_product_stock(billing_app):
    bill = billing_app
    rows = execute_fetchall(
        "SELECT pid, name, price, qty, status FROM product WHERE status='Active'"
    )
    assert len(rows) >= 1
    pid, name, price, stock = rows[0][0], rows[0][1], rows[0][2], rows[0][3]

    bill.var_pid.set(str(pid))
    bill.var_pname.set(name)
    bill.var_price.set(str(price))
    bill.var_qty.set("2")
    bill.var_stock.set(str(stock))

    with patch("billing.messagebox"):
        bill.add_update_cart()

    bill.var_cname.set("Test Customer")
    bill.var_contact.set("1234567890")

    with patch("billing.messagebox"):
        bill.generate_bill()

    updated = execute_fetchone("SELECT qty, status FROM product WHERE pid=?", (pid,))
    assert updated is not None
    assert int(updated[0]) == int(stock) - 2
    assert updated[1] == "Active"


def test_billing_sell_all_sets_inactive(billing_app):
    bill = billing_app
    rows = execute_fetchall(
        "SELECT pid, name, price, qty, status FROM product WHERE status='Active'"
    )
    assert len(rows) >= 1
    pid, name, price, stock = rows[0][0], rows[0][1], rows[0][2], rows[0][3]

    bill.var_pid.set(str(pid))
    bill.var_pname.set(name)
    bill.var_price.set(str(price))
    bill.var_qty.set(str(stock))
    bill.var_stock.set(str(stock))

    with patch("billing.messagebox"):
        bill.add_update_cart()

    bill.var_cname.set("Test Customer")
    bill.var_contact.set("9999999999")

    with patch("billing.messagebox"):
        bill.generate_bill()

    updated = execute_fetchone("SELECT qty, status FROM product WHERE pid=?", (pid,))
    assert updated is not None
    assert updated[0] == "0"
    assert updated[1] == "Inactive"
