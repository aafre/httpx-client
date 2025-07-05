# apiclient/client.py
from config.api_config import APIConfig
import httpx
from typing import Callable, Type, Any, Optional
from pydantic import BaseModel, ValidationError

import time
from functools import wraps


class APIClient:
    """
    Synchronous API client for making HTTP requests with retry capabilities,
    response validation, and post-processing.
    """
    
    def __init__(
        self,
        config: APIConfig,
        post_process_func: Optional[Callable[[Any], Any]] = None,
    ):
        """
        Initialize the API client with the given configuration.
        
        Args:
            config: Configuration for the API client
            post_process_func: Optional function to post-process API responses
        """
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
        """Get the current post-processing function."""
        return self._post_process_func

    @post_process_func.setter
    def post_process_func(self, func: Optional[Callable[[Any], Any]]):
        """Set the post-processing function."""
        self._post_process_func = func

    def _process_response(
        self, response: httpx.Response, schema: Type[BaseModel] = None
    ) -> Any:
        """
        Process the HTTP response, optionally validating with a schema and applying
        post-processing.
        
        Args:
            response: The HTTP response to process
            schema: Optional Pydantic model for validating the response data
            
        Returns:
            The processed response data
            
        Raises:
            ValueError: If schema validation fails
        """
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
        """
        Attempt the request with retries if it fails.
        
        Args:
            method: The HTTP method to use (get, post, put, delete, patch)
            endpoint: The API endpoint to call
            **kwargs: Additional arguments to pass to the request
            
        Returns:
            The HTTP response
            
        Raises:
            httpx.RequestError: If the request fails after all retries
            ValueError: If an unsupported HTTP method is specified
        """
        for _ in range(self.retries):
            try:
                if method == "get":
                    return self.client.get(endpoint, **kwargs)
                elif method == "post":
                    return self.client.post(endpoint, **kwargs)
                elif method == "put":
                    return self.client.put(endpoint, **kwargs)
                elif method == "delete":
                    return self.client.delete(endpoint, **kwargs)
                elif method == "patch":
                    return self.client.patch(endpoint, **kwargs)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
            except httpx.RequestError:
                time.sleep(1)
        raise httpx.RequestError(
            f"Request to {endpoint} failed after {self.retries} retries"
        )

    def get(self, endpoint: str, schema: Type[BaseModel] = None, **kwargs) -> Any:
        """
        Perform a GET request to the specified endpoint.
        
        Args:
            endpoint: The API endpoint to call
            schema: Optional Pydantic model for response validation
            **kwargs: Additional arguments to pass to the request
            
        Returns:
            Processed response data
            
        Raises:
            httpx.RequestError: If the request fails after all retries
            httpx.HTTPStatusError: If the response has an error status code
        """
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
        """
        Perform a POST request to the specified endpoint.
        
        Args:
            endpoint: The API endpoint to call
            data: Optional form data to send
            json: Optional JSON data to send
            schema: Optional Pydantic model for response validation
            **kwargs: Additional arguments to pass to the request
            
        Returns:
            Processed response data
            
        Raises:
            httpx.RequestError: If the request fails after all retries
            httpx.HTTPStatusError: If the response has an error status code
        """
        response = self._retry_request("post", endpoint, data=data, json=json, **kwargs)
        response.raise_for_status()
        return self._process_response(response, schema)

    def put(
        self,
        endpoint: str,
        data: Any = None,
        json: Any = None,
        schema: Type[BaseModel] = None,
        **kwargs,
    ) -> Any:
        """
        Perform a PUT request to the specified endpoint.
        
        Args:
            endpoint: The API endpoint to call
            data: Optional form data to send
            json: Optional JSON data to send
            schema: Optional Pydantic model for response validation
            **kwargs: Additional arguments to pass to the request
            
        Returns:
            Processed response data
            
        Raises:
            httpx.RequestError: If the request fails after all retries
            httpx.HTTPStatusError: If the response has an error status code
        """
        response = self._retry_request("put", endpoint, data=data, json=json, **kwargs)
        response.raise_for_status()
        return self._process_response(response, schema)
        
    def delete(
        self,
        endpoint: str,
        schema: Type[BaseModel] = None,
        **kwargs,
    ) -> Any:
        """
        Perform a DELETE request to the specified endpoint.
        
        Args:
            endpoint: The API endpoint to call
            schema: Optional Pydantic model for response validation
            **kwargs: Additional arguments to pass to the request
            
        Returns:
            Processed response data
            
        Raises:
            httpx.RequestError: If the request fails after all retries
            httpx.HTTPStatusError: If the response has an error status code
        """
        response = self._retry_request("delete", endpoint, **kwargs)
        response.raise_for_status()
        return self._process_response(response, schema)
        
    def patch(
        self,
        endpoint: str,
        data: Any = None,
        json: Any = None,
        schema: Type[BaseModel] = None,
        **kwargs,
    ) -> Any:
        """
        Perform a PATCH request to the specified endpoint.
        
        Args:
            endpoint: The API endpoint to call
            data: Optional form data to send
            json: Optional JSON data to send
            schema: Optional Pydantic model for response validation
            **kwargs: Additional arguments to pass to the request
            
        Returns:
            Processed response data
            
        Raises:
            httpx.RequestError: If the request fails after all retries
            httpx.HTTPStatusError: If the response has an error status code
        """
        response = self._retry_request("patch", endpoint, data=data, json=json, **kwargs)
        response.raise_for_status()
        return self._process_response(response, schema)

    def close(self):
        """Close the client and release resources."""
        self.client.close()

    def api_call(
        self, endpoint: str, method: str = "get", schema: Type[BaseModel] = None
    ):
        """
        Decorator for API calls to simplify usage patterns.
        
        Args:
            endpoint: The API endpoint to call
            method: HTTP method to use (get, post, put, delete, patch)
            schema: Optional Pydantic model for response validation
            
        Returns:
            Decorator function
            
        Example:
            @client.api_call("/users", method="get", schema=UserSchema)
            def get_users(limit=10, offset=0):
                return {"limit": limit, "offset": offset}
        """
        def decorator(func):
            @wraps(func)
            def wrapper(*args, **kwargs):
                if method.lower() == "get":
                    return self.get(endpoint, schema, **kwargs)
                elif method.lower() == "post":
                    return self.post(endpoint, **kwargs, schema=schema)
                elif method.lower() == "put":
                    return self.put(endpoint, **kwargs, schema=schema)
                elif method.lower() == "delete":
                    return self.delete(endpoint, schema, **kwargs)
                elif method.lower() == "patch":
                    return self.patch(endpoint, **kwargs, schema=schema)
                else:
                    raise ValueError(f"Unsupported HTTP method: {method}")
            return wrapper
        return decorator