import asyncio
import logging
import time

from aiohttp import ClientError, ClientSession

from accuweather import (
    AccuWeather,
    ApiError,
    InvalidApiKeyError,
    InvalidCoordinatesError,
    RequestsExceededError,
)

#for use with accuweather API
API_KEY = "boA10L9ACMVoFVfUXykXE6G9hiiEPxGr"

class Forecast:
    def __init__(self, curr_time = time.localtime(), latitude = 35.198284, longitude = -111.651299):
        #initialize attributes
        self.latitude = latitude
        self.longitude = longitude
        self.curr_time = curr_time
        self.weather_temp = [0] * 13

        #gather initial information on class creation for weather_temp
        loop = asyncio.new_event_loop()
        loop.run_until_complete(self.accuClient())
        loop.close()
        
    async def accuClient(self):
        async with ClientSession() as websession:
            
            #initialize temp variables
            weather_temp = [0] * 13

            #create object of type accuweather
            accuweather = AccuWeather(
                API_KEY,
                websession,
                latitude=self.latitude,
                longitude=self.longitude,
                language="en",
            )

            #retrieve all weather information
            current_conditions = await accuweather.async_get_current_conditions()
            forecast_hourly = await accuweather.async_get_hourly_forecast(
                hours=12, metric=True
            )

            #Place temperatures in array and current temps
            weather_temp[0] = current_conditions['Temperature']['Metric']['Value']
            for index in range (1, 13):
                weather_temp[index] = forecast_hourly[index]['Temperature']['Value']

            #assign attribute weather_temp as a list of temps
            self.weather_temp = weather_temp

    def getLatitude(self):
        print(self.latitude)

    def getLongitude(self):
        print(self.longitude)

    def getTime(self):
        print(self.curr_time)

    def getTemperatureCelsius(self):
        #Returns a list of temperatures in Celsius for the current through next 12 hours (13 total items)
        return self.weather_temp

    def getTemperatureFahrenheit(self):
        #Returns a list of temperatures in Fahrenheit for the current through next 12 hours (13 total items)
        temps_fahrenheit = [0] * 13

        #convert each item to fahrenheit
        for index in range (0, 13):
            temps_fahrenheit[index] = self.weather_temp[index] * (9/5) + 32 #Celsius to Fahrenheit formula
            
        return temps_fahrenheit