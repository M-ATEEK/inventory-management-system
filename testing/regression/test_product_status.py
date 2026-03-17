# product status set to Inactive when stock sold out

from unittest.mock import patch

from db_utils import execute_fetchone


def test_product_status_inactive_when_sold_out(billing_app):
    bill = billing_app
    row = execute_fetchone(
        "SELECT pid, name, price, qty, status FROM product WHERE name='Widget' AND status='Active'"
    )
    assert row is not None
    pid, name, price, stock, _ = row[0], row[1], row[2], row[3], row[4]
    bill.cart_list = [[str(pid), name, str(price), str(stock), str(stock)]]

    with patch("billing.messagebox"):
        bill.bill_middle()

    updated = execute_fetchone("SELECT qty, status FROM product WHERE pid=?", (pid,))
    assert updated is not None
    assert updated[0] == "0"
    assert updated[1] == "Inactive"
