import pytest
from httpx import ASGITransport, AsyncClient


@pytest.mark.asyncio
async def test_weather_endpoint(override_dependencies):
    """
    Integration test for the /weather/ endpoint using FastAPI's dependency override
    and HTTPX's AsyncClient with ASGITransport.

    Verifies:
    1. Request with short token (length < 32) → returns 401 Unauthorized.
    2. Request without token → returns 403 Forbidden.
    3. Request with valid token (length = 32) → returns 200 OK.
    4. Valid response contains:
        - a list of weather entries
        - each entry includes correct city
        - temperature field is a float
    """
    app = override_dependencies
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as ac:
        # Test: short token → unauthorized
        response = await ac.get("/weather/?city=Kyiv", headers={"x-token": "x" * 30})
        assert response.status_code == 401

        # Test: no token → forbidden
        response = await ac.get("/weather/?city=Kyiv")
        assert response.status_code == 403

        # Test: valid token → success
        response = await ac.get("/weather/?city=Kyiv", headers={"x-token": "x" * 32})
        assert response.status_code == 200

        # Validate response data structure
        data = response.json()
        assert isinstance(data, list)
        assert data[0]["city"] == "Kyiv"
        assert all(isinstance(i["temperature"], float) for i in data)
