from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
import requests
from datetime import datetime
from pprint import pprint


def get_weather(lat, lon, exclude='', unit='metric'):
    url = 'https://api.openweathermap.org/data/2.5/onecall'
    params = {'lat': lat, 'lon': lon, 'exclude': exclude, 'appid': '9f89938697ac4339dfc5ef3bac378dda', "units": unit}
    weather = requests.get(url, params)
    return weather.json()

def geocoder(location):
    url = 'https://api.opencagedata.com/geocode/v1/json'
    params = {'q':location, 'key': 'c45cd28450d24dd68b7621cd85165dbd'}
    geocode = requests.get(url, params)
    lat = geocode.json()['results'][-1]['geometry']['lat']
    lon = geocode.json()['results'][-1]['geometry']['lng']
    pprint(geocode.json()['results'][-1])
    print(lat, lon)
    return lat, lon

weather = get_weather(*geocoder("Owerri, Nigeria"))
city = "Owerri"

# Create your views here.
def home(request):
    global weather
    global city

    if request.method == "POST":
        location= request.POST['location']
        lat, lon = geocoder(location)
        #print(exclude)
        return 
        weather = get_weather(lat, lon)
        return HttpResponseRedirect('/home/')

    if request.method == "GET":
        print(weather['current'])
        result = {}
        result['time'] = datetime.strftime(datetime.fromtimestamp(weather['current']['dt']), "%a, %I:%M %p")
        result['city'] = city
        result['current_description'] = weather['current']['weather'][0]['description']
        result['current_temp'] = weather['current']['temp']
        result['humidity'] = weather["current"]['humidity']
        result['cloudiness'] = weather['current']['clouds']
        result['rain'] = weather['current']['rain']['1h'] if weather['current'].get('rain') else "N/A"
        result['wind'] = weather['current']['wind_speed']
        result['current_icon'] = weather['current']['weather'][0]['icon']
        result['daily'] = []
        for i, day in enumerate(weather['daily'][1:]):
            print(day['dt'])
            max = round(day['temp']['max'])
            min= round(day['temp']['min'])
            day = datetime.strftime(datetime.fromtimestamp(day['dt']), "%A")
            result['daily'].append({'day':day ,"min": min, "max": max})

        #return JsonResponse(result)

        return render(request, "weather.html", {'weather': weather})
