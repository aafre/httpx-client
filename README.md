# APIClient
🚀 APIClient - A flexible and powerful API client supporting both synchronous and asynchronous operations, built with httpx and pydantic for schema validation. 🌐🔧

[![CI](https://github.com/yourusername/api_client/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/api_client/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/api_client.svg)](https://badge.fury.io/py/api_client)
[![Python versions](https://img.shields.io/pypi/pyversions/api_client.svg)](https://pypi.org/project/api_client/)

## Features ✨
- Dual Mode: Supports both synchronous and asynchronous operations.
- Schema Validation: Easily validate API responses with pydantic.
- Retry Mechanism: Built-in retry mechanism for robust error handling.
- Post-Processing: Custom post-processing of API responses.
- Highly Customizable: Tailor the client to your needs with flexible configurations.

## Installation
You can install the package via pip:

```sh
pip install api_client
```


## Usage

### Configuration
Create a configuration class using `pydantic` to define your API settings:


```python
from pydantic import BaseModel, AnyHttpUrl
from typing import Optional, Union

class APIConfig(BaseModel):
    base_url: AnyHttpUrl
    retries: int = 3
    timeout: float = 5.0
    headers: Optional[dict] = None
    auth_type: Optional[str] = None
    auth_credentials: Optional[Union[str, dict]] = None

```

### Synchronous Client
Use the synchronous client for blocking operations:

```python
from api_client.core.sync_client import APIClient
from api_client.config import APIConfig

config = APIConfig(base_url="https://api.example.com")
client = APIClient(config)

response = client.get("/endpoint")
print(response)

```

### Asynchronous Client
Use the asynchronous client for non-blocking operations:

```python
import asyncio
from api_client.core.async_client import AsyncAPIClient
from api_client.config import APIConfig

config = APIConfig(base_url="https://api.example.com")
client = AsyncAPIClient(config)

async def main():
    response = await client.get("/endpoint")
    print(response)

asyncio.run(main())
```


### Custom Post-Processing
Define a custom post-processing function to modify API responses:

```python
def post_process(data):
    return data["result"]

config = APIConfig(base_url="https://api.example.com")
client = APIClient(config, post_process_func=post_process)

response = client.get("/endpoint")
print(response)
```

## Contributing

Feel free to open issues or submit pull requests for any changes you would like to see. Contributions are welcome!

## License

This project is licensed under the MIT License. See the LICENSE file for details.