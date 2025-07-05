# HTTPX Client

A simple wrapper around HTTPX with basic retry logic and Pydantic validation.

[![CI](https://github.com/aafre/APIClient/actions/workflows/ci.yml/badge.svg)](https://github.com/aafre/APIClient/actions/workflows/ci.yml)

## Status: No Longer in Development

This package was an experiment in creating a higher-level API client wrapper. After evaluation, we've determined that HTTPX alone provides sufficient functionality for most use cases.

**We recommend using [HTTPX](https://www.python-httpx.org/) directly instead.**

## Installation

```bash
pip install httpx-client
```

## Basic Usage

```python
from api_client.core.sync_client import SyncAPIClient
from api_client.config.api_config import APIConfig

config = APIConfig(base_url="https://api.example.com")
client = SyncAPIClient(config)

response = client.get("/users")
```

## Why Not This Package?

HTTPX already provides excellent functionality:

```python
import httpx

# This is cleaner and more direct:
with httpx.Client(base_url="https://api.example.com") as client:
    response = client.get("/users")
    data = response.json()
```

For retry logic, use [httpx-retry](https://github.com/JWCook/requests-retry).  
For validation, use [Pydantic](https://pydantic.dev/) directly.

## License

MIT License - see [LICENSE](LICENSE) file for details.