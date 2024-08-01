# apiclient/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import AnyHttpUrl, Field
from typing import Optional, Union


class APIConfig(BaseSettings):
    """
    APIConfig is a configuration class for APIClient. It defines the necessary
    settings to initialize and configure an API client. The class uses pydantic's
    BaseSettings to support environment variable overrides, making it suitable
    for various deployment environments.

    Attributes:
        base_url (AnyHttpUrl): The base URL for the API.
        retries (int): The number of retry attempts for failed requests. Default is 3.
        timeout (float): The timeout for API requests in seconds. Default is 5.0.
        headers (Optional[dict]): Optional headers to include in API requests. Default is None.
        auth_type (Optional[str]): The type of authentication ('basic', 'bearer', or 'api_key'). Default is None.
        auth_credentials (Optional[Union[str, dict]]): The credentials for authentication (string for API key or dict for username/password). Default is None.
    """

    base_url: AnyHttpUrl
    retries: int = 3
    timeout: float = 5.0
    headers: Optional[dict] = None
    auth_type: Optional[str] = Field(default=None, env="API_AUTH_TYPE")
    auth_credentials: Optional[Union[str, dict]] = Field(
        default=None, env="API_AUTH_CREDENTIALS"
    )

    model_config = SettingsConfigDict(
        env_prefix="API_",  # Prefix for environment variables
        env_file=".env",  # Optionally load from a .env file
        env_file_encoding="utf-8",
    )
