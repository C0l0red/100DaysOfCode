import requests
from datetime import datetime

url = 'https://api.openweathermap.org/data/2.5/onecall'
params = {'lat': 5.489059, 'lon': 7.017588, 'exclude': 'hourly,daily', 'appid': '9f89938697ac4339dfc5ef3bac378dda'}
weather = request.get(url, params)
json = weather.json()
print("lat: ", json['lat'])
print("long: ", json['lon'])
print("timezone: ", json['timezone'])
print('current time: ', )

