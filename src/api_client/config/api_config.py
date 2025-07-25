# api_client/config/api_config.py
import json
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, Field
from pydantic.functional_validators import field_validator
from typing import Optional, Union


class APIConfig(BaseSettings):
    """
    APIConfig is a configuration class for APIClient. It defines the necessary
    settings to initialize and configure an API client. The class uses pydantic's
    BaseSettings to support environment variable overrides, making it suitable
    for various deployment environments.

    Attributes:
        base_url (str): The base URL for the API, always with a trailing slash.
        retries (int): The number of retry attempts for failed requests. Default is 3.
        timeout (float): The timeout for API requests in seconds. Default is 5.0.
        headers (Optional[dict]): Optional headers to include in API requests. Default is None.
        auth_type (Optional[str]): The type of authentication ('basic', 'bearer', or 'api_key'). Default is None.
        auth_credentials (Optional[Union[str, dict]]): The credentials for authentication (string for API key or dict for username/password). Default is None.
    """

    base_url: str = Field(..., env="API_BASE_URL")
    retries: int = 3
    timeout: float = Field(default=5.0, env="API_TIMEOUT")
    headers: Optional[dict] = None
    auth_type: Optional[str] = Field(default=None, env="API_AUTH_TYPE")
    auth_credentials: Optional[Union[str, dict]] = Field(
        default=None, env="API_AUTH_CREDENTIALS"
    )

    @field_validator("base_url", mode="before")
    def validate_base_url(cls, value: str) -> str:
        # Ensure it's a proper HTTP URL with trailing slash
        if not isinstance(value, str) or not value.startswith(("http://", "https://")):
            raise ValueError(f"Invalid URL provided: {value}")
        # Strip extra slashes, then add exactly one
        stripped = value.rstrip("/")
        return stripped + "/"

    @field_validator("auth_credentials", mode="before")
    def parse_auth_credentials(cls, value):
        # If credentials come as JSON string, parse to dict
        if isinstance(value, str):
            try:
                return json.loads(value)
            except json.JSONDecodeError:
                return value
        return value

    model_config = SettingsConfigDict(
        env_prefix="API_",         # Prefix for environment variables
        env_file=".env",           # Optionally load from a .env file
        env_file_encoding="utf-8",
    )
