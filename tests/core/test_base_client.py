# api_client/core/tests/test_base_client.py
import pytest
import httpx
from httpx import Response
from api_client.core.base_client import BaseAPIClient
from api_client.config.api_config import APIConfig
from pydantic import BaseModel
import json


class DummySchema(BaseModel):
    key: str


def post_process(data):
    return {"processed_key": data["key"]}


@pytest.fixture
def client():
    cfg = APIConfig(base_url="https://api.example.com/")
    return BaseAPIClient(cfg)


def test_base_api_client_initialization(client):
    assert client.config.base_url == "https://api.example.com/"
    assert client.retries == 3
    assert client.post_process_func is None


def test_base_api_client_initialization_with_post_process():
    cfg = APIConfig(base_url="https://api.example.com/")
    cli = BaseAPIClient(cfg, post_process_func=post_process)
    assert cli.post_process_func == post_process


def test_process_response_with_schema(client):
    response = Response(200, json={"key": "value"})
    data = client._process_response(response, schema=DummySchema)
    assert isinstance(data, DummySchema)
    assert data.key == "value"


def test_process_response_with_invalid_schema(client):
    response = Response(200, json={"invalid_key": "value"})
    with pytest.raises(ValueError):
        client._process_response(response, schema=DummySchema)


def test_process_response_without_schema_returns_dict(client):
    response = Response(200, json={"foo": "bar"})
    data = client._process_response(response)
    assert isinstance(data, dict)
    assert data == {"foo": "bar"}


def test_process_response_non_json_body(client):
    # httpx.Response.json() will raise json.JSONDecodeError
    response = Response(200, content=b"not a json")
    with pytest.raises(json.JSONDecodeError):
        client._process_response(response)


def test_process_response_with_post_process(client):
    cfg = APIConfig(base_url="https://api.example.com/")
    cli = BaseAPIClient(cfg, post_process_func=post_process)
    response = Response(200, json={"key": "value"})
    data = cli._process_response(response)
    assert data == {"processed_key": "value"}


def test_retry_request_success(client):
    class MockClient:
        def get(self, url, *args, **kwargs):
            return Response(200, json={"key": "value"})

    client.client = MockClient()
    response = client._retry_request(client.client.get, "/test")
    assert response.json() == {"key": "value"}


def test_retry_request_failure(client):
    class MockClient:
        def get(self, url, *args, **kwargs):
            raise httpx.RequestError("Request failed")

    client.client = MockClient()
    with pytest.raises(httpx.RequestError):
        client._retry_request(client.client.get, "/test")


def test_retry_request_intermittent_failure(client):
    calls = []

    def flaky(url):
        calls.append(True)
        if len(calls) < 2:
            raise httpx.RequestError("fail")
        return Response(200, json={})

    client.retries = 3
    result = client._retry_request(flaky, "/")
    assert isinstance(result, Response)
    assert len(calls) == 2


def test_sync_client_close_and_reuse_raises():
    from api_client.core.sync_client import SyncAPIClient

    cfg = APIConfig(base_url="https://api.example.com/")
    cli = SyncAPIClient(cfg)
    cli.close()
    with pytest.raises(RuntimeError):
        # After closing, underlying client cannot send requests
        cli.client.get("/")

