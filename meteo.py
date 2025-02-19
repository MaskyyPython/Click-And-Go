import requests
import json
# 9d449b3de540e17b79c60aa699f08123
def get_weather_data(city, api_m):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_m}"
    response = requests.get(url)
    data = json.loads(response.text)
    return data
