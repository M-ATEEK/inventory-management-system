from db_utils import execute_fetchall, execute_fetchone, execute_update


def test_fetchall_returns_rows_after_insert(seeded_db):
    rows = execute_fetchall("SELECT * FROM users WHERE email=?", ("test@example.com",))
    assert len(rows) == 1
    assert rows[0][2] == "test@example.com"


def test_fetchone_returns_none_when_no_match(seeded_db):
    result = execute_fetchone("SELECT * FROM users WHERE email=?", ("nonexistent@test.com",))
    assert result is None


def test_execute_update_insert_and_verify(test_db):
    from create_db import create_db
    create_db()
    execute_update("INSERT INTO users(name,email,password) VALUES(?,?,?)", ("Alice", "alice@test.com", "secret"))
    row = execute_fetchone("SELECT * FROM users WHERE email=?", ("alice@test.com",))
    assert row is not None
    assert row[1] == "Alice"
