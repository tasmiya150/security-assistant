import pytest
import sys
sys.path.insert(0, "app")

from app.password_checker import check_strength, generate_password
from app.database import init_db, save_check, get_recent_checks
import os

# ── Password strength ──────────────────────────────────────────────────────────

def test_common_password_is_weak():
    result = check_strength("123456")
    assert result["strength"] == "Weak"
    assert result["score"] == 0

def test_short_password_is_weak():
    result = check_strength("ab1!")
    assert result["strength"] in ("Weak", "Medium")
    assert result["score"] < 10  # short password should never be Strong

def test_medium_password():
    result = check_strength("Hello123")
    assert result["strength"] in ("Medium", "Strong")

def test_strong_password():
    result = check_strength("SecureP@ss99")
    assert result["strength"] == "Strong"
    assert result["score"] == 10

def test_no_special_char_lowers_score():
    result = check_strength("HelloWorld1")
    assert result["score"] < 10

def test_suggestions_returned_for_weak():
    result = check_strength("abc")
    assert len(result["reasons"]) > 0

# ── Password generator ─────────────────────────────────────────────────────────

def test_generated_password_default_length():
    pw = generate_password()
    assert len(pw) == 12

def test_generated_password_custom_length():
    pw = generate_password(20)
    assert len(pw) == 20

def test_generated_password_uniqueness():
    passwords = {generate_password() for _ in range(10)}
    assert len(passwords) > 1  # Should not all be the same

# ── Database ───────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def setup_db(tmp_path, monkeypatch):
    import app.database as database
    monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    init_db()

def test_save_and_retrieve_check():
    save_check("hashed_pw", "Strong", 10)
    rows = get_recent_checks(1)
    assert len(rows) == 1
    assert rows[0]["strength"] == "Strong"
    assert rows[0]["score"] == 10

def test_history_limit():
    for i in range(15):
        save_check(f"hash_{i}", "Weak", 2)
    rows = get_recent_checks(10)
    assert len(rows) == 10