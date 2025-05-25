# api_client/config/tests/test_api_config.py

import pytest
from pydantic import ValidationError
from api_client.config.api_config import APIConfig


def test_default_values():
    config = APIConfig(base_url="https://api.example.com")
    assert config.retries == 3
    assert config.timeout == 5.0
    assert config.headers is None
    assert config.auth_type is None
    assert config.auth_credentials is None


def test_env_variable_override(monkeypatch):
    monkeypatch.setenv("API_BASE_URL", "https://api.override.com")
    monkeypatch.setenv("API_RETRIES", "5")
    monkeypatch.setenv("API_TIMEOUT", "10.0")
    monkeypatch.setenv("API_AUTH_TYPE", "bearer")
    monkeypatch.setenv("API_AUTH_CREDENTIALS", "override_token")

    config = APIConfig()

    assert config.base_url == "https://api.override.com/"
    assert config.retries == 5
    assert config.timeout == 10.0
    assert config.auth_type == "bearer"
    assert config.auth_credentials == "override_token"


def test_invalid_url():
    with pytest.raises(ValidationError):
        APIConfig(base_url="invalid_url")


def test_headers_type_validation():
    with pytest.raises(ValidationError):
        APIConfig(base_url="https://api.example.com/", headers="not a dict")


def test_missing_base_url():
    with pytest.raises(ValidationError):
        APIConfig()  # base_url is required


def test_allow_zero_retries():
    # Zero retries means “no retry attempts”
    config = APIConfig(base_url="https://api.example.com/", retries=0)
    assert config.retries == 0


def test_allow_zero_timeout():
    # Zero timeout means “wait indefinitely”
    config = APIConfig(base_url="https://api.example.com/", timeout=0)
    assert config.timeout == 0


def test_basic_auth_parsing(monkeypatch):
    monkeypatch.setenv("API_AUTH_TYPE", "basic")
    monkeypatch.setenv(
        "API_AUTH_CREDENTIALS", '{"username": "user", "password": "pass"}'
    )
    config = APIConfig(base_url="https://api.example.com/")
    assert config.auth_type == "basic"
    assert config.auth_credentials == {"username": "user", "password": "pass"}


def test_api_key_auth(monkeypatch):
    monkeypatch.setenv("API_AUTH_TYPE", "api_key")
    monkeypatch.setenv("API_AUTH_CREDENTIALS", "api_key_value")
    config = APIConfig(base_url="https://api.example.com/")
    assert config.auth_type == "api_key"
    assert config.auth_credentials == "api_key_value"


def test_invalid_json_auth_credentials(monkeypatch):
    monkeypatch.setenv("API_AUTH_TYPE", "basic")
    monkeypatch.setenv("API_AUTH_CREDENTIALS", "not a json")
    config = APIConfig(base_url="https://api.example.com/")
    # Should leave the string unchanged
    assert config.auth_credentials == "not a json"
