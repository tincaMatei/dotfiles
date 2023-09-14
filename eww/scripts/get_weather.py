import json
import sys
import os
from buienradar.buienradar import (get_data, parse_data)
from buienradar.constants import (CONTENT, RAINCONTENT, SUCCESS, DATA, 
                                  CONDITION, EXACT, TEMPERATURE, FEELTEMPERATURE,
                                  PRECIPITATION, DETAILED, HUMIDITY)

returned = {
    "weather": "",
    "weather_msg": "Unknown",
    "temperature": "?",
    "temperaturedelta": "?",
    "rain": "?",
    "humidity": "?",
    "error": "success"
}

icons = {
    "clear": "",
    "partlycloudy": "",
    "cloudy": "",
    "partlycloudy-fog": "",
    "partlycloudy-light-rain": "",
    "partlycloudy-rain": "",
    "light-rain": "",
    "rainy": "",
    "snowy-rainy": "",
    "partlylcloudy-light-snow": "",
    "partlylcloudy-snow": "",
    "light-snow": "",
    "snowy": "",
    "partlycloudy-lightning": "",
    "lightning": ""
}

# Put the cities that you want in here with the good latitudes and longitudes
cities = {
    "city": (0.0000), (0.0000)
}

try:
    environ = os.environ
    city = environ["EWW_WEATHER_CITY"]

    timeframe = 120
    lat, lon = cities[city]

    res = get_data(latitude = lat, longitude = lon)
    if res.get(SUCCESS):
        data = res[CONTENT]
        raindata = res[RAINCONTENT]

        result = parse_data(data, raindata, lat, lon, timeframe)
        
        weather = result[DATA][CONDITION][DETAILED]
        weathermsg = result[DATA][CONDITION][EXACT]
        temperature = result[DATA][TEMPERATURE]
        feeltemperature = result[DATA][FEELTEMPERATURE]
        precipitation = result[DATA][PRECIPITATION]
        humidity = result[DATA][HUMIDITY]

        if weather is None:
            raise Exception("Weather is None")
        if temperature is None:
            raise Exception("Temperature is None")
        if feeltemperature is None:
            raise Exception("Feel temperature is None")
        if precipitation is None:
            raise Exception("Precipitation is None")
        if weathermsg is None:
            raise Exception("Weather message is None")
        if humidity is None:
            raise Exception("Humidity is None")

        weather = icons[weather]
        
        returned = {
            "weather": weather,
            "weather_msg": weathermsg,
            "temperature": temperature,
            "temperaturedelta": feeltemperature - temperature,
            "rain": precipitation,
            "humidity": humidity
        }
except Exception as e:
    returned["error"] = str(e)

print(json.dumps(returned))

