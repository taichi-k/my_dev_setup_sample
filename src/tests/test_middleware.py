from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import Request, Response

from app.middleware.access_log import access_log_middleware


async def test_access_log_middleware():
    """アクセスログmiddlewareのテスト"""
    # Mock Request
    request = MagicMock(spec=Request)
    request.method = "GET"
    request.url.path = "/test"
    request.url.query = "param=value"
    request.headers.get.side_effect = lambda key, default: {
        "user-agent": "test-agent",
        "x-forwarded-for": "192.168.1.1",
    }.get(key, default)
    request.client.host = "127.0.0.1"

    # Mock Response
    response = MagicMock(spec=Response)
    response.status_code = 200

    # Mock call_next
    call_next = AsyncMock(return_value=response)

    # Execute middleware
    result = await access_log_middleware(request, call_next)

    # Assertions
    assert result == response
    call_next.assert_called_once_with(request)


async def test_access_log_middleware_with_exception():
    """例外が発生した場合のmiddlewareテスト"""
    request = MagicMock(spec=Request)
    request.method = "POST"
    request.url.path = "/error"
    request.url.query = ""
    request.headers.get.return_value = None
    request.client.host = "127.0.0.1"

    # Mock call_next to raise exception
    call_next = AsyncMock(side_effect=Exception("Test error"))

    # Execute and expect exception
    with pytest.raises(Exception):
        await access_log_middleware(request, call_next)
