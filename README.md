# APIClient
🚀 APIClient - A flexible and powerful API client supporting both synchronous and asynchronous operations, built with httpx and pydantic for schema validation. 🌐🔧

[![CI](https://github.com/yourusername/api_client/actions/workflows/ci.yml/badge.svg)](https://github.com/aafre/api_client/actions/workflows/ci.yml)
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


### Custom Post-Processing hooks
Define a custom post-processing function to modify API responses:

```python
def post_process(data):
    return data["result"]

config = APIConfig(base_url="https://api.example.com")
client = APIClient(config, post_process_func=post_process)

response = client.get("/endpoint")
print(response)
```


Example: 

```python
# Automatic post-process result from API to extract nested data
 def extract_payload(data):
     return data.get("payload", {})

config = APIConfig(base_url="https://api.example.com")
client = APIClient(config, post_process_func=extract_payload)
```


### Feature Status Table

| **Feature**                              | **Status**           | **Priority**         | **Comments**                                                                                                                                                      |
|------------------------------------------|----------------------|----------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Schema Validation**                    | 🟡 **Partially Done** | **Must**            | Implemented in `_process_response`, but requires `schemas.py` for complete validation functionality.                                                            |
| **Configuration via APIConfig**          | 🔴 **Pending**       | **Must**            | The `APIConfig` class is mentioned but not fully implemented in the provided code.                                                                              |
| **Flexible Request Methods (GET, POST)** | 🟡 **Partially Done** | **Must**            | GET and POST are implemented for both sync and async clients, but other methods like PUT, DELETE are not implemented yet.                                       |
| **Error Handling**                       | 🟡 **Partially Done** | **Must**            | Some error handling is implemented, but lacks differentiation between retryable and non-retryable errors; custom exceptions are needed.                          |
| **Detailed Exceptions**                  | 🔴 **Pending**       | **Must**            | Introduce custom exceptions like `ClientError`, `ServerError`, and `ValidationError`.                                                                            |
| **Retry Backoff Strategy**               | 🔵 **Future Update** | **Future Update**    | Retries use a fixed 1-second delay; exponential backoff is not implemented.                                                                                     |
| **Custom Retry Conditions**              | 🔴 **Pending**       | **Must**            | Retry conditions are fixed and not user-configurable.                                                                                                           |
| **Client Lifecycle Management**          | 🟡 **Partially Done** | **Must**            | `close` is implemented for sync/async clients, but proper resource management is necessary to prevent resource leaks.                                            |
| **Custom Authentication Handling**       | 🔴 **Pending**       | **Must**            | `auth_type` and `auth_credentials` in `APIConfig` are placeholders; no implementation is provided in the core clients.                                          |
| **Custom Headers Support**               | ✅ **Implemented**   | **Must**            | Headers can be set via `APIConfig`.                                                                                                                             |
| **Timeout Configuration**                | ✅ **Implemented**   | **Must**            | Timeout is configurable via `APIConfig`.                                                                                                                        |
| **Base URL Configuration**               | ✅ **Implemented**   | **Must**            | Base URL is configurable via `APIConfig`.                                                                                                                       |
| **Global Middleware/Interceptors**       | 🔵 **Future Update** | **Future Update**    | Useful for logging, error transformations, or request preprocessing.                                                                                            |
| **Rate-Limiting Handling**               | 🔵 **Future Update** | **Future Update**    | No rate-limiting mechanism is implemented; support `429 Too Many Requests` headers.                                                                             |
| **API Client Decorators**                | 🟡 **Partially Done** | **Must**            | `api_call` decorator is defined in `APIClient`, but its usage is unclear and lacks examples or thorough testing.                                                |
| **Test Cases for Core Features**         | 🔴 **Pending**       | **Must**            | Test cases are not provided or mentioned.                                                                                                                       |
| **HTTPX Integration**                    | ✅ **Implemented**   | **Done**            | Fully leverages `httpx` for sync and async HTTP operations.                                                                                                     |
| **Pluggable Serialization/Deserialization** | 🔴 **Pending**    | **Must**            | Support for custom serialization/deserialization logic, especially for non-JSON APIs.                                                                           |
| **Dynamic URL Building**                 | 🔴 **Pending**       | **Must**            | Add helper methods for constructing complex URLs with query parameters.                                                                                         |
| **Session Persistence**                  | 🔴 **Pending**       | **Must**            | Maintain state across requests (e.g., cookies, headers).                                                                                                        |
| **Asynchronous Request Streaming**       | 🔴 **Pending**       | **Must**            | Add support for APIs that return large responses or streams (e.g., file downloads).                                                                             |
| **Pip Installation Support**             | 🔴 **Pending**       | **Must**            | Package structure seems compatible with pip installation, but `setup.py` or equivalent is not included.                                                        |

---

### Legend:
- ✅ **Implemented**: Fully implemented as per the requirements.
- 🟡 **Partially Done**: Some aspects are implemented, but additional work is needed.
- 🔴 **Pending**: Not implemented and requires development.
- 🔵 **Future Update**: Planned for future releases.

---

### Development Roadmap & Milestones

1. **schemas.py & validation hooks**  
   Define `schemas.py` and wire up response validation.  
2. **APIConfig enhancements**  
   Implement full `APIConfig` with timeouts, retries, and `backoff_factor`.  
3. **All HTTP methods**  
   Add PUT, DELETE, and PATCH alongside existing GET/POST.  
4. **Core retry, backoff & user-configurable conditions**  
   Support exponential backoff and custom retry predicates.  
5. **Error handling & detailed exceptions**  
   Differentiate retryable vs. non-retryable errors and introduce `ClientError`, `ServerError`, etc.  
6. **Authentication handlers & token refresh**  
   Implement `auth_type`/`auth_credentials` for OAuth2, API-keys, and custom schemes.  
7. **Client lifecycle improvements**  
   Ensure proper `close`/`aclose` and cleanup of HTTP resources.  
8. **Pluggable serialization & dynamic URL builder**  
   Support custom serializers and helper utilities for query-string and path construction.  
9. **Session persistence**  
   Reuse `httpx.Client`/`AsyncClient` for connection pooling, cookies, and stateful headers.  
10. **Asynchronous request streaming**  
    Enable streaming large responses or file downloads without loading into memory.  
11. **Test suite for core features**  
    Write unit and integration tests covering all client workflows.  
12. **Packaging**  
    Add `setup.py`/`pyproject.toml` and publish the package to PyPI.  


## 🤝 Contributing

Feel free to open issues or submit pull requests for any changes you would like to see. Contributions are welcome!

## License

This project is licensed under the MIT License. See the LICENSE file for details.


