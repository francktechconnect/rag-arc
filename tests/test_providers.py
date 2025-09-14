import os
import pytest
from app.providers import LLMProvider


def test_openrouter_headers_real_env():
    api_key = os.getenv("OPENROUTER_API_KEY")
    model_name = os.getenv("OPENROUTER_MODEL", "meta-llama/llama-3.1-8b-instruct:free")

    if not api_key:
        pytest.skip("OPENROUTER_API_KEY not set in environment")

    provider = LLMProvider()
    headers, url, model = provider._hosted_headers()

    assert "Authorization" in headers
    assert headers["Authorization"] == f"Bearer {api_key}"
    assert "openrouter.ai" in url
    assert model == model_name


def test_openrouter_headers(monkeypatch):
    monkeypatch.setenv("OPENROUTER_API_KEY", "test_key")
    monkeypatch.setenv("OPENROUTER_MODEL", "meta-llama/test-model")
       
    provider = LLMProvider()
    headers, url, model = provider._hosted_headers()

    assert "Authorization" in headers
    assert headers["Authorization"] == "Bearer test_key"
    assert "openrouter.ai" in url
    assert model == "meta-llama/test-model"


def test_togetherai_headers(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.setenv("TOGETHER_API_KEY", "together_key")
    monkeypatch.setenv("TOGETHER_MODEL", "meta-llama/Together-Test")

    provider = LLMProvider()
    headers, url, model = provider._hosted_headers()

    assert headers["Authorization"] == "Bearer together_key"
    assert "together.xyz" in url
    assert model == "meta-llama/Together-Test"


def test_huggingface_headers(monkeypatch):
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("TOGETHER_API_KEY", raising=False)
    monkeypatch.setenv("HF_API_KEY", "hf_key")
    monkeypatch.setenv("HF_MODEL", "test/hf-model")

    provider = LLMProvider()
    headers, url, model = provider._hosted_headers()

    assert headers["Authorization"] == "Bearer hf_key"
    assert "huggingface.co" in url
    assert model is None  # HF doesn’t use a model param in chat API


def test_no_credentials(monkeypatch):
    # clear all
    monkeypatch.delenv("OPENROUTER_API_KEY", raising=False)
    monkeypatch.delenv("TOGETHER_API_KEY", raising=False)
    monkeypatch.delenv("HF_API_KEY", raising=False)

    provider = LLMProvider()
    with pytest.raises(RuntimeError, match="No hosted LLM credentials found"):
        provider._hosted_headers()
