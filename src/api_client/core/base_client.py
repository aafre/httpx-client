import httpx
import logging
from typing import Callable, Type, Any, Optional
from pydantic import BaseModel, ValidationError
from api_client.config.api_config import APIConfig
import time

logger = logging.getLogger(__name__)


class BaseAPIClient:
    """
    Base class for API clients, providing common functionality such as request handling,
    response processing, and retry logic.
    """

    def __init__(
        self,
        config: APIConfig,
        post_process_func: Optional[Callable[[Any], Any]] = None,
    ):
        self.config = config
        self.retries = config.retries
        self.post_process_func = post_process_func
        # Ensure base_url is a plain str when passed to httpx
        self.client = httpx.Client(
            base_url=str(config.base_url),
            timeout=config.timeout,
            headers=config.headers or {},
        )
        logger.debug(f"Initialized API Client with config: {config}")

    @property
    def post_process_func(self) -> Optional[Callable[[Any], Any]]:
        return self._post_process_func

    @post_process_func.setter
    def post_process_func(self, func: Optional[Callable[[Any], Any]]):
        self._post_process_func = func
        logger.debug(f"Set post-process function: {func}")

    def _process_response(
        self, response: httpx.Response, schema: Type[BaseModel] = None
    ) -> Any:
        """
        Process the response from the API, optionally validating it against a pydantic schema
        and applying a post-processing function.
        """
        # Avoid accessing response.url when no Request is set (e.g. in tests)
        try:
            url = response.url
        except Exception:
            url = "<unknown>"
        logger.debug(f"Processing response from {url}")

        try:
            data = response.json()
            logger.debug(f"Response JSON: {data}")

            if schema:
                data = schema.model_validate(data)
                logger.debug(f"Validated response with schema: {schema}")

            if self.post_process_func:
                data = self.post_process_func(data)
                logger.debug(f"Post-processed response data: {data}")

            return data

        except ValidationError as e:
            logger.error(f"Response validation error: {e}")
            raise ValueError(f"Response validation error: {e}")

    def _retry_request(self, method: Callable, *args, **kwargs) -> httpx.Response:
        """
        Retry the request for a specified number of attempts if it fails.
        """
        for attempt in range(1, self.retries + 1):
            try:
                name = getattr(method, "__name__", "anonymous")
                logger.info(f"Attempt {attempt} for {name} with args={args}, kwargs={kwargs}")
                return method(*args, **kwargs)
            except httpx.RequestError as e:
                logger.warning(f"Request attempt {attempt} failed: {e}")
                time.sleep(1)

        error_msg = f"Request failed after {self.retries} retries"
        logger.error(error_msg)
        raise httpx.RequestError(error_msg)

    async def _retry_request_async(self, method: Callable, *args, **kwargs) -> httpx.Response:
        """
        Retry the async request for a specified number of attempts if it fails.
        """
        import asyncio
        
        for attempt in range(1, self.retries + 1):
            try:
                name = getattr(method, "__name__", "anonymous")
                logger.info(f"Attempt {attempt} for {name} with args={args}, kwargs={kwargs}")
                return await method(*args, **kwargs)
            except httpx.RequestError as e:
                logger.warning(f"Request attempt {attempt} failed: {e}")
                await asyncio.sleep(1)

        error_msg = f"Request failed after {self.retries} retries"
        logger.error(error_msg)
        raise httpx.RequestError(error_msg)
