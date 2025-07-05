import httpx
from typing import Callable, Optional, Type, Any
from api_client.core.base_client import BaseAPIClient
from api_client.config.api_config import APIConfig
from pydantic import BaseModel


class AsyncAPIClient(BaseAPIClient):
    def __init__(
        self,
        config: APIConfig,
        post_process_func: Optional[Callable[[Any], Any]] = None,
    ):
        super().__init__(config, post_process_func)
        self.client = httpx.AsyncClient(
            base_url=str(config.base_url),
            timeout=config.timeout,
            headers=config.headers or {},
        )

    async def get(self, endpoint: str, schema: Type[BaseModel] = None, **kwargs) -> Any:
        response = await self._retry_request_async(self.client.get, endpoint, **kwargs)
        response.raise_for_status()
        return self._process_response(response, schema)

    async def post(
        self,
        endpoint: str,
        data: Any = None,
        json: Any = None,
        schema: Type[BaseModel] = None,
        **kwargs,
    ) -> Any:
        response = await self._retry_request_async(
            self.client.post, endpoint, data=data, json=json, **kwargs
        )
        response.raise_for_status()
        return self._process_response(response, schema)

    async def put(
        self,
        endpoint: str,
        data: Any = None,
        json: Any = None,
        schema: Type[BaseModel] = None,
        **kwargs,
    ) -> Any:
        response = await self._retry_request_async(
            self.client.put, endpoint, data=data, json=json, **kwargs
        )
        response.raise_for_status()
        return self._process_response(response, schema)

    async def patch(
        self,
        endpoint: str,
        data: Any = None,
        json: Any = None,
        schema: Type[BaseModel] = None,
        **kwargs,
    ) -> Any:
        response = await self._retry_request_async(
            self.client.patch, endpoint, data=data, json=json, **kwargs
        )
        response.raise_for_status()
        return self._process_response(response, schema)

    async def delete(self, endpoint: str, schema: Type[BaseModel] = None, **kwargs) -> Any:
        response = await self._retry_request_async(self.client.delete, endpoint, **kwargs)
        response.raise_for_status()
        return self._process_response(response, schema)

    async def head(self, endpoint: str, **kwargs) -> httpx.Response:
        response = await self._retry_request_async(self.client.head, endpoint, **kwargs)
        response.raise_for_status()
        return response

    async def options(self, endpoint: str, **kwargs) -> httpx.Response:
        response = await self._retry_request_async(self.client.options, endpoint, **kwargs)
        response.raise_for_status()
        return response

    async def close(self):
        await self.client.aclose()
