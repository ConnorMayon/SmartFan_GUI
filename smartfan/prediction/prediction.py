from smartfan.app.gui import SmartFanApp
from smartfan.data.local_weather import Climate
from smartfan.data.online_weather import Forecast
import time
import datetime

class Prediction():
    def __init__(self, app: SmartFanApp, in_climate: Climate, out_climate: Climate, forecast: Forecast):
        self.app = app
        self.in_climate = in_climate
        self.out_climate = out_climate
        self.forecast = forecast

    def predict(self) -> bool:
        """
        Predictive algorithm that determines whether or not to active fans based on temperature data
        and user preferences.
        Returns boolean to representing whether fan should be turned on or off
        """
        # get temperatures
        in_temp = self.in_climate.getTempF()
        out_temp = self.out_climate.getTempF()
        range_min = self.app.min_temp
        range_max = self.app.max_temp
        forecast_temp = self.forecast.getTemperatureFahrenheit()
        curr_time = time.localtime()
        preferred_time = datetime.time(hour=self.app.hour, minute=self.app.ten + self.app.min)

        # temporary data analysis code to determine whether temperature is increasing or decreating
        min_temp = out_temp
        max_temp = out_temp
        num_dec = 0
        num_inc = 0
        prev_temp = out_temp
        for forecast_hour in range(1, 7):
            if forecast_temp[forecast_hour] > prev_temp:
                num_inc += 1
            elif forecast_temp[forecast_hour] < prev_temp:
                num_dec += 1
            if forecast_temp[forecast_hour] > max_temp:
                max_temp = forecast_temp[forecast_hour]
            if forecast_temp[forecast_hour] < min_temp:
                min_temp = forecast_temp[forecast_hour]
            prev_temp = forecast_temp[forecast_hour]

        temp_increasing = num_inc > num_dec and max_temp > range_max
        temp_decreasing = num_inc < num_dec and min_temp < range_min

        # if within preffered cooling time
        if curr_time >= preferred_time:
            # if temp not in range, activate iff outside temperature is closer to desired range
            if in_temp not in range(range_min, range_max):
                if in_temp > range_max and out_temp < in_temp:
                    return True
                elif in_temp < range_min and out_temp > in_temp:
                    return True
                else:
                    return False
            
            # if temp in range, activate if forecasted temperates are moving out of range and
            # there is room to move in the opposite direction of forecast
            else:
                if temp_increasing and out_temp < in_temp and in_temp > range_min:
                    return True
                elif temp_decreasing and out_temp > in_temp and in_temp < range_max:
                    return True
                else: 
                    return False
        else:
            return False