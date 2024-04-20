import unittest
from accuweather import InvalidCoordinatesError
from smartfan.data.online_weather import Forecast

class TestOnlineWeather(unittest.TestCase):
    def test_coordinates(self):
        Forecast(latitude=35.198284, longitude=-111.651299)

    def test_coordinates2(self):
        Forecast(latitude=41.8781, longitude=87.6298)

    def test_coordinates3(self):
        Forecast(latitude=40.7128, longitude=74.0060)

    def test_coordinates4(self):
        with self.assertRaises(InvalidCoordinatesError):
            Forecast(latitude=67, longitude=190)

    def test_coordinates5(self):
        with self.assertRaises(InvalidCoordinatesError):
            Forecast(latitude=360, longitude=-360)

    def test_coordinates6(self):
        with self.assertRaises(InvalidCoordinatesError):
            Forecast(latitude=-100, longitude=159)

    def test_get_temperature(self):
        flagstaff = Forecast(latitude=35.198284, longitude=-111.651299)
        (self.assertIsInstance(hour, int) for hour in flagstaff.getTemperatureFahrenheit())

    def test_get_temperature2(self):
        chicago = Forecast(latitude=41.8781, longitude=87.6298)
        (self.assertIsInstance(hour, int) for hour in chicago.getTemperatureFahrenheit())

    def test_get_temperature3(self):
        new_york = Forecast(latitude=40.7128, longitude=74.0060)
        (self.assertIsInstance(hour, int) for hour in new_york.getTemperatureCelsius())
    