"""Tests for authentication."""
import pytest
from swarmforge.security.auth import hash_password, verify_password, generate_api_key, create_access_token, decode_access_token

class TestAuth:
    def test_hash_and_verify(self):
        hashed = hash_password("my-password")
        assert verify_password("my-password", hashed) is True
        assert verify_password("wrong-password", hashed) is False

    def test_generate_api_key(self):
        raw, hashed = generate_api_key()
        assert raw.startswith("sf_")
        assert len(raw) > 40
        assert len(hashed) == 64  # SHA256

    def test_jwt_token(self):
        token = create_access_token({"sub": "test-user"})
        decoded = decode_access_token(token)
        assert decoded is not None
        assert decoded["sub"] == "test-user"

    def test_jwt_invalid(self):
        assert decode_access_token("invalid-token") is None
