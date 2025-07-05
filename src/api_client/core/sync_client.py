from api_client.config.api_config import APIConfig
from api_client.core.base_client import BaseAPIClient
import httpx
from typing import Callable, Optional, Type, Any


from pydantic import BaseModel


class SyncAPIClient(BaseAPIClient):
    def __init__(
        self,
        config: APIConfig,
        post_process_func: Optional[Callable[[Any], Any]] = None,
    ):
        super().__init__(config, post_process_func)
        self.client = httpx.Client(
            base_url=str(config.base_url),
            timeout=config.timeout,
            headers=config.headers or {},
        )

    def get(self, endpoint: str, schema: Type[BaseModel] = None, **kwargs) -> Any:
        response = self._retry_request(self.client.get, endpoint, **kwargs)
        response.raise_for_status()
        return self._process_response(response, schema)

    def post(
        self,
        endpoint: str,
        data: Any = None,
        json: Any = None,
        schema: Type[BaseModel] = None,
        **kwargs
    ) -> Any:
        response = self._retry_request(
            self.client.post, endpoint, data=data, json=json, **kwargs
        )
        response.raise_for_status()
        return self._process_response(response, schema)

    def put(
        self,
        endpoint: str,
        data: Any = None,
        json: Any = None,
        schema: Type[BaseModel] = None,
        **kwargs
    ) -> Any:
        response = self._retry_request(
            self.client.put, endpoint, data=data, json=json, **kwargs
        )
        response.raise_for_status()
        return self._process_response(response, schema)

    def patch(
        self,
        endpoint: str,
        data: Any = None,
        json: Any = None,
        schema: Type[BaseModel] = None,
        **kwargs
    ) -> Any:
        response = self._retry_request(
            self.client.patch, endpoint, data=data, json=json, **kwargs
        )
        response.raise_for_status()
        return self._process_response(response, schema)

    def delete(self, endpoint: str, schema: Type[BaseModel] = None, **kwargs) -> Any:
        response = self._retry_request(self.client.delete, endpoint, **kwargs)
        response.raise_for_status()
        return self._process_response(response, schema)

    def head(self, endpoint: str, **kwargs) -> httpx.Response:
        response = self._retry_request(self.client.head, endpoint, **kwargs)
        response.raise_for_status()
        return response

    def options(self, endpoint: str, **kwargs) -> httpx.Response:
        response = self._retry_request(self.client.options, endpoint, **kwargs)
        response.raise_for_status()
        return response

    def close(self):
        self.client.close()
