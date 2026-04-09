"""Sample test to verify pytest setup."""
import pytest


def test_sample():
    """Basic test to verify pytest is working."""
    assert True


@pytest.mark.asyncio
async def test_async_sample():
    """Basic async test to verify pytest-asyncio is working."""
    assert True
