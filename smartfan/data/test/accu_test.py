"""Example of usage."""
import asyncio
import logging

from aiohttp import ClientError, ClientSession

from accuweather import (
    AccuWeather,
    ApiError,
    InvalidApiKeyError,
    InvalidCoordinatesError,
    RequestsExceededError,
)

LATITUDE = 35.198284
LONGITUDE = -111.651299
API_KEY = "boA10L9ACMVoFVfUXykXE6G9hiiEPxGr"

logging.basicConfig(level=logging.DEBUG)


async def main():
    """Run main function."""
    async with ClientSession() as websession:
        try:
            accuweather = AccuWeather(
                API_KEY,
                websession,
                latitude=LATITUDE,
                longitude=LONGITUDE,
                language="en",
            )
            current_conditions = await accuweather.async_get_current_conditions()
            forecast_daily = await accuweather.async_get_daily_forecast(
                days=5, metric=True
            )
            forecast_hourly = await accuweather.async_get_hourly_forecast(
                hours=12, metric=True
            )
        except (
            ApiError,
            InvalidApiKeyError,
            InvalidCoordinatesError,
            ClientError,
            RequestsExceededError,
        ) as error:
            print(f"Error: {error}")
        else:
            test = current_conditions['Temperature']['Metric']['Value']
            print(f"Location: {accuweather.location_name} ({accuweather.location_key})")
            print(f"Current: {test} Celsius")
            for i in range (0, 12):
                print(f"Forecast hourly: {forecast_hourly[i]['Temperature']['Value']}")

loop = asyncio.new_event_loop()
loop.run_until_complete(main())
loop.close()
