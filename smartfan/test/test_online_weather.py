import pytest
from accuweather import InvalidCoordinatesError
from smartfan.data.online_weather import Forecast

class TestOnlineWeather():
    flagstaff: Forecast
    chicago: Forecast
    new_york: Forecast

    def run_tests(self):
        self.test_coordinates()
        self.test_coordinates2()
        self.test_coordinates3()
        self.test_coordinates4()
        self.test_coordinates5()
        self.test_coordinates6()

    def test_coordinates(self):
        self.flagstaff = Forecast(latitude=35.198284, longitude=-111.651299)

    def test_coordinates2(self):
        self.chicago = Forecast(latitude=41.8781, longitude=87.6298)

    def test_coordinates3(self):
        self.new_york = Forecast(latitude=40.7128, longitude=74.0060)

    def test_coordinates4(self):
        with pytest.raises(InvalidCoordinatesError):
            Forecast(latitude=67, longitude=190)

    def test_coordinates5(self):
        with pytest.raises(InvalidCoordinatesError):
            Forecast(latitude=360, longitude=-360)

    def test_coordinates6(self):
        with pytest.raises(InvalidCoordinatesError):
            Forecast(latitude=-100, longitude=159)