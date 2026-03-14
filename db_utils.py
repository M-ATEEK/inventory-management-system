import os
import sqlite3
from contextlib import contextmanager

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "ims.db")


def _get_db_path():
    return os.environ.get("IMS_DB_PATH", DB_PATH)


@contextmanager
def get_connection():
    conn = sqlite3.connect(database=_get_db_path())
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def execute_fetchall(query: str, params: tuple = ()) -> list:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchall()


def execute_fetchone(query: str, params: tuple = ()):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(query, params)
        return cur.fetchone()


def execute_update(query: str, params: tuple = ()) -> None:
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute(query, params)


def populate_treeview(treeview, rows: list) -> None:
    treeview.delete(*treeview.get_children())
    for row in rows:
        treeview.insert("", "end", values=row)
