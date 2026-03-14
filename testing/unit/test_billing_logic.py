# real products from DB, fetch, add to cart, bill_update

from unittest.mock import patch

from db_utils import execute_fetchall


def test_bill_amount_and_discount_from_real_products(billing_app):
    bill = billing_app
    rows = execute_fetchall(
        "SELECT pid,name,price,qty,status FROM product WHERE status='Active'"
    )
    assert len(rows) >= 1
    pid, name, price, stock, status = rows[0][0], rows[0][1], rows[0][2], rows[0][3], rows[0][4]

    bill.var_pid.set(str(pid))
    bill.var_pname.set(name)
    bill.var_price.set(str(price))
    bill.var_qty.set("2")
    bill.var_stock.set(str(stock))

    with patch("billing.messagebox"):
        bill.add_update_cart()

    assert bill.bill_amnt == 21.0  
    assert bill.discount == 1.05  
    assert bill.net_pay == 19.95


def test_bill_amount_multiple_products_from_db(billing_app):
    bill = billing_app
    rows = execute_fetchall(
        "SELECT pid,name,price,qty,status FROM product WHERE status='Active'"
    )
    assert len(rows) >= 2

    with patch("billing.messagebox"):
        for row in rows[:2]:
            pid, name, price, stock = row[0], row[1], row[2], row[3]
            bill.var_pid.set(str(pid))
            bill.var_pname.set(name)
            bill.var_price.set(str(price))
            bill.var_qty.set("1")
            bill.var_stock.set(str(stock))
            bill.add_update_cart()

    expected_amnt = 15.50
    expected_discount = (expected_amnt * 5) / 100  # 0.775
    expected_net = expected_amnt - expected_discount

    assert abs(bill.bill_amnt - expected_amnt) < 0.01
    assert abs(bill.discount - expected_discount) < 0.01
    assert abs(bill.net_pay - expected_net) < 0.01
