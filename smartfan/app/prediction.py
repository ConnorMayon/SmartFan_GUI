def predict(range_min: int, range_max: int, in_temp: int, out_temp: int, forecast_temp = None) -> bool:
    """
    Predictive algorithm that determines whether or not to active fans based on temperature data
    and user preferences.
    Returns boolean to representing whether fan should be turned on or off
    """

    if forecast_temp is not None:
        # temporary data analysis code to determine whether temperature is increasing or decreasing
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

    # if temp not in range, activate iff outside temperature is closer to desired range
    if in_temp not in range(range_min, range_max):
        if in_temp > range_max and out_temp < in_temp - 1:
            return True
        elif in_temp < range_min and out_temp > in_temp + 1:
            return True
        else:
            return False
        
    # if temp in range, activate if forecasted temperates are moving out of range and
    # there is room to move in the opposite direction of forecast
    elif forecast_temp is not None:
        if temp_increasing and out_temp < in_temp and in_temp > range_min:
            return True
        elif temp_decreasing and out_temp > in_temp and in_temp < range_max:
            return True
        else: 
            return False
