import pytest
import httpx
from httpx import Response
from api_client.core.sync_client import SyncAPIClient
from api_client.config.api_config import APIConfig
from pydantic import BaseModel
from unittest.mock import Mock, patch


class TestSchema(BaseModel):
    message: str
    status: int


@pytest.fixture
def config():
    return APIConfig(base_url="https://api.example.com/")


@pytest.fixture
def client(config):
    return SyncAPIClient(config)


class TestSyncClientHTTPMethods:
    """Test all HTTP methods for the synchronous client"""
    
    def test_get_method(self, client):
        with patch.object(client, '_retry_request') as mock_retry:
            mock_response = Mock()
            mock_response.json.return_value = {"message": "success", "status": 200}
            mock_retry.return_value = mock_response
            
            result = client.get("/test")
            
            mock_retry.assert_called_once()
            mock_response.raise_for_status.assert_called_once()
            assert result == {"message": "success", "status": 200}
    
    def test_post_method(self, client):
        with patch.object(client, '_retry_request') as mock_retry:
            mock_response = Mock()
            mock_response.json.return_value = {"message": "created", "status": 201}
            mock_retry.return_value = mock_response
            
            result = client.post("/test", json={"data": "test"})
            
            mock_retry.assert_called_once()
            mock_response.raise_for_status.assert_called_once()
            assert result == {"message": "created", "status": 201}
    
    def test_put_method(self, client):
        with patch.object(client, '_retry_request') as mock_retry:
            mock_response = Mock()
            mock_response.json.return_value = {"message": "updated", "status": 200}
            mock_retry.return_value = mock_response
            
            result = client.put("/test/1", json={"data": "updated"})
            
            mock_retry.assert_called_once()
            mock_response.raise_for_status.assert_called_once()
            assert result == {"message": "updated", "status": 200}
    
    def test_patch_method(self, client):
        with patch.object(client, '_retry_request') as mock_retry:
            mock_response = Mock()
            mock_response.json.return_value = {"message": "patched", "status": 200}
            mock_retry.return_value = mock_response
            
            result = client.patch("/test/1", json={"field": "new_value"})
            
            mock_retry.assert_called_once()
            mock_response.raise_for_status.assert_called_once()
            assert result == {"message": "patched", "status": 200}
    
    def test_delete_method(self, client):
        with patch.object(client, '_retry_request') as mock_retry:
            mock_response = Mock()
            mock_response.json.return_value = {"message": "deleted", "status": 204}
            mock_retry.return_value = mock_response
            
            result = client.delete("/test/1")
            
            mock_retry.assert_called_once()
            mock_response.raise_for_status.assert_called_once()
            assert result == {"message": "deleted", "status": 204}
    
    def test_head_method(self, client):
        with patch.object(client, '_retry_request') as mock_retry:
            mock_response = Mock()
            mock_retry.return_value = mock_response
            
            result = client.head("/test")
            
            mock_retry.assert_called_once()
            mock_response.raise_for_status.assert_called_once()
            assert result == mock_response
    
    def test_options_method(self, client):
        with patch.object(client, '_retry_request') as mock_retry:
            mock_response = Mock()
            mock_retry.return_value = mock_response
            
            result = client.options("/test")
            
            mock_retry.assert_called_once()
            mock_response.raise_for_status.assert_called_once()
            assert result == mock_response


class TestSyncClientWithSchema:
    """Test HTTP methods with schema validation"""
    
    def test_get_with_schema(self, client):
        with patch.object(client, '_retry_request') as mock_retry:
            mock_response = Mock()
            mock_response.json.return_value = {"message": "success", "status": 200}
            mock_retry.return_value = mock_response
            
            result = client.get("/test", schema=TestSchema)
            
            mock_retry.assert_called_once()
            mock_response.raise_for_status.assert_called_once()
            assert isinstance(result, TestSchema)
            assert result.message == "success"
            assert result.status == 200
    
    def test_post_with_schema(self, client):
        with patch.object(client, '_retry_request') as mock_retry:
            mock_response = Mock()
            mock_response.json.return_value = {"message": "created", "status": 201}
            mock_retry.return_value = mock_response
            
            result = client.post("/test", json={"data": "test"}, schema=TestSchema)
            
            assert isinstance(result, TestSchema)
            assert result.message == "created"
            assert result.status == 201


class TestSyncClientErrorHandling:
    """Test error handling for sync client"""
    
    def test_http_error_handling(self, client):
        with patch.object(client, '_retry_request') as mock_retry:
            mock_response = Mock()
            mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
                "404 Not Found", request=Mock(), response=mock_response
            )
            mock_retry.return_value = mock_response
            
            with pytest.raises(httpx.HTTPStatusError):
                client.get("/not-found")
    
    def test_request_error_handling(self, client):
        with patch.object(client, '_retry_request') as mock_retry:
            mock_retry.side_effect = httpx.RequestError("Connection failed")
            
            with pytest.raises(httpx.RequestError):
                client.get("/test")


class TestSyncClientRequestParameters:
    """Test various request parameters and configurations"""
    
    def test_get_with_params(self, client):
        with patch.object(client, '_retry_request') as mock_retry:
            mock_response = Mock()
            mock_response.json.return_value = {"results": []}
            mock_retry.return_value = mock_response
            
            client.get("/test", params={"page": 1, "limit": 10})
            
            # Verify the call was made with the correct parameters
            args, kwargs = mock_retry.call_args
            assert "params" in kwargs
            assert kwargs["params"] == {"page": 1, "limit": 10}
    
    def test_post_with_data_and_json(self, client):
        with patch.object(client, '_retry_request') as mock_retry:
            mock_response = Mock()
            mock_response.json.return_value = {"id": 1}
            mock_retry.return_value = mock_response
            
            # Test with JSON data
            client.post("/test", json={"name": "test"})
            args, kwargs = mock_retry.call_args
            assert kwargs["json"] == {"name": "test"}
            
            # Test with form data
            client.post("/test", data={"name": "test"})
            args, kwargs = mock_retry.call_args
            assert kwargs["data"] == {"name": "test"}
    
    def test_custom_headers(self, client):
        with patch.object(client, '_retry_request') as mock_retry:
            mock_response = Mock()
            mock_response.json.return_value = {}
            mock_retry.return_value = mock_response
            
            client.get("/test", headers={"Custom-Header": "value"})
            
            args, kwargs = mock_retry.call_args
            assert kwargs["headers"] == {"Custom-Header": "value"}