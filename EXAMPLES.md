# HTTPX Client Examples

This file contains detailed examples and documentation that was previously in the README.

## Detailed Usage Examples

### Synchronous Client

```python
from api_client.core.sync_client import SyncAPIClient
from api_client.config.api_config import APIConfig

# Advanced configuration
config = APIConfig(
    base_url="https://jsonplaceholder.typicode.com",
    timeout=30.0,
    retries=5,
    headers={
        "User-Agent": "MyApp/1.0",
        "Accept": "application/json"
    }
)

client = SyncAPIClient(config)

# All HTTP methods
users = client.get("/users")
user = client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
client.put("/users/1", json={"name": "Alice Updated"})
client.patch("/users/1", json={"email": "new-email@example.com"})
client.delete("/users/1")

# HEAD and OPTIONS for metadata
headers = client.head("/users")
options = client.options("/users")
```

### Asynchronous Client

```python
import asyncio
from api_client.core.async_client import AsyncAPIClient

async def main():
    client = AsyncAPIClient(config)
    
    # Same interface, async execution
    users = await client.get("/users")
    user = await client.post("/users", json={"name": "Bob"})
    await client.put("/users/1", json={"name": "Bob Updated"})
    await client.patch("/users/1", json={"email": "bob@example.com"})
    await client.delete("/users/1")
    
    # HEAD and OPTIONS for metadata
    headers = await client.head("/users")
    options = await client.options("/users")
    
    # Always close the client when done
    await client.close()

asyncio.run(main())
```

### Response Validation with Pydantic

```python
from pydantic import BaseModel
from typing import List

class User(BaseModel):
    id: int
    name: str
    email: str

class UserList(BaseModel):
    users: List[User]

# Automatic validation and type safety
users: UserList = client.get("/users", schema=UserList)
user: User = client.post("/users", json={"name": "Charlie"}, schema=User)

# Type-safe access
print(f"First user: {users.users[0].name}")
```

### Custom Response Processing

```python
def extract_data(response_json):
    """Extract nested data from API responses"""
    return response_json.get("data", response_json)

client = SyncAPIClient(config, post_process_func=extract_data)

# Response automatically processed
clean_data = client.get("/api/users")  # Already extracted from {"data": [...]}
```

### Authentication Examples

```python
# Bearer token
config = APIConfig(
    base_url="https://api.example.com",
    auth_type="bearer",
    auth_credentials="your-token-here"
)

# API key
config = APIConfig(
    base_url="https://api.example.com",
    headers={"X-API-Key": "your-api-key"}
)

# Basic auth
config = APIConfig(
    base_url="https://api.example.com",
    auth_type="basic",
    auth_credentials={"username": "user", "password": "pass"}
)
```

## Development Commands

```bash
# Install dependencies
uv sync --locked --all-extras

# Run tests
uv run pytest

# Run specific test files
uv run pytest tests/core/test_sync_client.py -v

# Format code
uv run black .

# Lint code
uv run ruff check --fix .

# Run with coverage
uv run pytest --cov=src/api_client
```

## Features Implementation Status

| Feature | Status | Description |
|---------|--------|-------------|
| **Complete HTTP Methods** | ✅ | GET, POST, PUT, PATCH, DELETE, HEAD, OPTIONS |
| **Sync/Async Dual Mode** | ✅ | True synchronous and asynchronous support |
| **Automatic Retries** | ✅ | Configurable retry logic with backoff |
| **Pydantic Integration** | ✅ | Native schema validation for responses |
| **Custom Post-Processing** | ✅ | Transform responses with custom functions |
| **Configuration Management** | ✅ | Environment-aware settings with validation |
| **Type Safety** | ✅ | Full type hints and mypy compatibility |
| **Comprehensive Testing** | ✅ | 100% test coverage for all features |

## Alternative Recommendations

Instead of this package, consider these battle-tested options:

### Direct HTTPX Usage
```python
import httpx
from httpx_retry import HTTPXRetry

retry_strategy = HTTPXRetry(
    max_retries=3,
    backoff_factor=1.0
)

with httpx.Client(
    base_url="https://api.example.com",
    timeout=30.0
) as client:
    response = client.get("/users")
    data = response.json()
```

### With Pydantic Validation
```python
import httpx
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

with httpx.Client(base_url="https://api.example.com") as client:
    response = client.get("/users/1")
    user = User.model_validate(response.json())
```

### Async HTTPX
```python
import asyncio
import httpx

async def fetch_users():
    async with httpx.AsyncClient(base_url="https://api.example.com") as client:
        response = await client.get("/users")
        return response.json()

users = asyncio.run(fetch_users())
```