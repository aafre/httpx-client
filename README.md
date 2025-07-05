# HTTPX Client

Lightweight HTTPX wrapper providing retry logic, Pydantic validation, and unified sync/async API client interfaces.

[![CI](https://github.com/aafre/httpx-client/actions/workflows/ci.yml/badge.svg)](https://github.com/aafre/httpx-client/actions/workflows/ci.yml)

## Features

- **Dual Mode**: Complete synchronous and asynchronous client support
- **Schema Validation**: Automatic response validation with Pydantic models
- **Retry Logic**: Built-in configurable retry mechanism with backoff
- **Post-Processing**: Custom response transformation hooks
- **Type Safety**: Full type hints and mypy compatibility
- **Configuration Management**: Environment-aware settings with validation

## Installation

```bash
pip install httpx-client
```

## Quick Examples

### Basic Usage

```python
from api_client.core.sync_client import SyncAPIClient
from api_client.config.api_config import APIConfig

# Configure the client
config = APIConfig(
    base_url="https://jsonplaceholder.typicode.com",
    timeout=10.0,
    retries=3
)

client = SyncAPIClient(config)

# Use all HTTP methods
users = client.get("/users")
user = client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
client.put("/users/1", json={"name": "Alice Updated"})
client.patch("/users/1", json={"email": "new-email@example.com"})
client.delete("/users/1")
```

### Async Support

```python
import asyncio
from api_client.core.async_client import AsyncAPIClient

async def main():
    client = AsyncAPIClient(config)
    
    users = await client.get("/users")
    user = await client.post("/users", json={"name": "Bob"})
    
    await client.close()

asyncio.run(main())
```

### Pydantic Schema Validation

```python
from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str

# Automatic validation and type safety
user: User = client.get("/users/1", schema=User)
print(f"User: {user.name} ({user.email})")
```

### Advanced Configuration

```python
config = APIConfig(
    base_url="https://api.example.com",
    timeout=30.0,
    retries=5,
    headers={
        "User-Agent": "MyApp/1.0",
        "Authorization": "Bearer your-token"
    }
)
```

### Custom Response Processing

```python
def extract_data(response):
    return response.get("data", response)

client = SyncAPIClient(config, post_process_func=extract_data)
data = client.get("/api/users")  # Automatically extracts nested data
```

## Development

```bash
# Install dependencies
uv sync --locked --all-extras

# Run tests
uv run pytest

# Format and lint
uv run black .
uv run ruff check --fix .
```

## License

MIT License - see [LICENSE](LICENSE) file for details.

---

## Status: No Longer Maintained

This project was successfully completed and achieved all its original goals. However, it is no longer being actively maintained or developed. The functionality works as designed, but no new features or updates will be added.