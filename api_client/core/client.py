# apiclient/client.py
from config.api_config import APIConfig
import httpx
from typing import Callable, Type, Any, Optional
from pydantic import BaseModel, ValidationError

import time
from functools import wraps


class APIClient:
    def __init__(
        self,
        config: APIConfig,
        post_process_func: Optional[Callable[[Any], Any]] = None,
    ):
        self.config = config
        self.client = httpx.Client(
            base_url=config.base_url,
            timeout=config.timeout,
            headers=config.headers or {},
        )
        self.retries = config.retries
        self._post_process_func = post_process_func

    @property
    def post_process_func(self) -> Optional[Callable[[Any], Any]]:
        return self._post_process_func

    @post_process_func.setter
    def post_process_func(self, func: Optional[Callable[[Any], Any]]):
        self._post_process_func = func

    def _process_response(
        self, response: httpx.Response, schema: Type[BaseModel] = None
    ) -> Any:
        data = response.json()
        if schema:
            try:
                data = schema.parse_obj(data)
            except ValidationError as e:
                raise ValueError(f"Response validation error: {e}")
        if self.post_process_func:
            data = self.post_process_func(data)
        return data

    def _retry_request(self, method: str, endpoint: str, **kwargs):
        for _ in range(self.retries):
            try:
                if method == "get":
                    return self.client.get(endpoint, **kwargs)
                elif method == "post":
                    return self.client.post(endpoint, **kwargs)
                # Add other methods (put, delete) as needed
            except httpx.RequestError:
                time.sleep(1)
        raise httpx.RequestError(
            f"Request to {endpoint} failed after {self.retries} retries"
        )

    def get(self, endpoint: str, schema: Type[BaseModel] = None, **kwargs) -> Any:
        response = self._retry_request("get", endpoint, **kwargs)
        response.raise_for_status()
        return self._process_response(response, schema)

    def post(
        self,
        endpoint: str,
        data: Any = None,
        json: Any = None,
        schema: Type[BaseModel] = None,
        **kwargs,
    ) -> Any:
        response = self._retry_request("post", endpoint, data=data, json=json, **kwargs)
        response.raise_for_status()
        return self._process_response(response, schema)

    def close(self):
        self.client.close()

    def api_call(
        self, endpoint: str, method: str = "get", schema: Type[BaseModel] = None
    ):
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if method.lower() == "get":
                    return self.get(endpoint, schema, **kwargs)
                elif method.lower() == "post":
                    return self.post(endpoint, **kwargs, schema=schema)
                # Add other methods (put, delete) as needed

            return wrapper

        return decorator
