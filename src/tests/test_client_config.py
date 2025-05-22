import pytest
from onepasswordconnectsdk.config import ClientConfig
import httpx

def test_client_config_with_ca_file():
    config = ClientConfig(ca_file="path/to/ca.pem")
    args = config.get_client_args("https://test.com", {"Authorization": "Bearer token"}, 30.0)
    
    assert args["verify"] == "path/to/ca.pem"
    assert args["base_url"] == "https://test.com"
    assert args["headers"] == {"Authorization": "Bearer token"}
    assert args["timeout"] == 30.0

def test_client_config_with_kwargs():
    config = ClientConfig(
        ca_file="path/to/ca.pem",
        follow_redirects=True,
        timeout=60.0
    )
    args = config.get_client_args("https://test.com", {"Authorization": "Bearer token"}, 30.0)
    
    assert args["verify"] == "path/to/ca.pem"
    assert args["follow_redirects"] == True
    # kwargs should override default timeout
    assert args["timeout"] == 60.0

def test_client_config_verify_override():
    # When verify is explicitly set in kwargs, it should override ca_file
    config = ClientConfig(
        ca_file="path/to/ca.pem",
        verify=False
    )
    args = config.get_client_args("https://test.com", {"Authorization": "Bearer token"}, 30.0)
    
    assert args["verify"] == False

def test_client_config_no_ca_file():
    config = ClientConfig()
    args = config.get_client_args("https://test.com", {"Authorization": "Bearer token"}, 30.0)
    
    assert "verify" not in args
    assert args["base_url"] == "https://test.com"
    assert args["headers"] == {"Authorization": "Bearer token"}
    assert args["timeout"] == 30.0
