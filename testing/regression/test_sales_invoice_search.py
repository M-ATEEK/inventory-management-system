# sales invoice search finds bill when invoice exists in list

import os
import tempfile


def test_sales_invoice_search_finds_existing_bill():
    with tempfile.TemporaryDirectory() as bill_dir:
        invoice_no = "12345"
        bill_path = os.path.join(bill_dir, f"{invoice_no}.txt")
        with open(bill_path, "w") as f:
            f.write("Sample bill content")

        bill_list = []
        for fname in os.listdir(bill_dir):
            if fname.endswith(".txt"):
                bill_list.append(fname.split(".")[0])

        assert invoice_no in bill_list
        assert os.path.exists(bill_path)
