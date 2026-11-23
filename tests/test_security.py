from app.security import hash_password, verify_password

def test_hash_is_not_plaintext():
    assert hash_password("secret123") != "secret123"

def test_verify_roundtrip():
    h = hash_password("secret123")
    assert verify_password("secret123", h) is True
    assert verify_password("mauvais", h) is False
