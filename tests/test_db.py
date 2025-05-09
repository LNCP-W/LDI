from datetime import date, datetime, timedelta

import pytest
from db import DB


@pytest.mark.asyncio
async def test_set_weather(get_db: DB):
    """
    Test that verifies setting and retrieving a single weather entry.

    Steps:
    - Inserts a weather record for a specific city and timestamp.
    - Retrieves the weather data for that city and date.
    - Asserts that the record is correctly saved and matches input.

    Asserts:
    - The inserted weather record returns a valid integer ID.
    - The retrieved record is not None and matches city and temperature.
    """
    db = get_db
    now = datetime.now()
    city = "TestCity"
    temperature = 23.5

    weather_id = await db.set_weather(
        city=city, temperature=temperature, time_point=now
    )
    assert isinstance(weather_id, int)

    result = await db.get_weather(city=city, day=now.date())
    assert result is not None
    assert len(result) == 1
    assert result[0].city == city
    assert result[0].temperature == temperature


@pytest.mark.asyncio
async def test_get_weather(get_db: DB):
    """
    Test that verifies retrieving multiple weather entries for a city on a specific day.

    Steps:
    - Inserts two weather records for the same day but different times.
    - Fetches weather data for that day and city.
    - Ensures both records are present and ordered by descending time.

    Asserts:
    - At least two entries are returned.
    - Entries are ordered by time descending.
    - Each entry matches the specified city and has the correct date.
    """
    db = get_db
    today = date.today()
    city = "WeatherVille"
    time1 = datetime.combine(today, datetime.min.time()) + timedelta(hours=9)
    time2 = datetime.combine(today, datetime.min.time()) + timedelta(hours=15)

    await db.set_weather(city=city, temperature=20.1, time_point=time1)
    await db.set_weather(city=city, temperature=25.7, time_point=time2)

    weather_data = await db.get_weather(city=city, day=today)
    assert len(weather_data) >= 2
    assert (
        weather_data[0].time_point >= weather_data[1].time_point
    )  # ensure descending order
    for entry in weather_data:
        assert entry.city == city
        assert entry.time_point.date() == today
