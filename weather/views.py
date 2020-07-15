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

def geocoded(location):
    url = 'https://api.opencagedata.com/geocode/v1/json'
    params = {'q':location, 'key': 'c45cd28450d24dd68b7621cd85165dbd'}
    geocode = requests.get(url, params)
    lat = geocode.json()['results'][-1]['geometry']['lat']
    lon = geocode.json()['results'][-1]['geometry']['lng']
    return lat, lon

def geocoder(location):
    url = 'https://geocode.xyz'
    params = {"locate": location, 'geoit':"JSON"}
    r = requests.get(url, params)
    geocode = r.json()
    city = geocode['standard']['city']
    return city, geocode['latt'], geocode['longt']

#weather = get_weather(*geocoder("Abuja, Nigeria"))


# Create your views here.
def home(request, hour=None):
    if not request.session.get('weather'):
        city, *GEOCODE = geocoder("Abuja, Nigeria")
        request.session['weather'] = get_weather(*GEOCODE)
        request.session['city'] = city

    weather = request.session['weather']
    city = request.session['city']

    if not hour:
        focus = weather['current']

    if request.method == "POST":
        location= request.POST['location']
        city, *GEOCODE = geocoder(location)
        
        weather = get_weather(*GEOCODE)

        request.session['weather'] = weather
        request.session['city'] = city
        return HttpResponseRedirect('/weather/')

    if request.method == "GET":
        dt =  weather['timezone_offset'] + focus['dt']
        dt = datetime.fromtimestamp(dt)
        print(weather['timezone_offset'], focus['dt'])
        result = {}
        result['time'] = dt.strftime( "%a, %I:%M %p")
        if int(dt.strftime("%H")) in range(8, 20):
            result['con'], result['rev'] = "AM", "PM"
        else:
            result['con'], result['rev'] = "PM", "AM"
        result['city'] = city
        result['current_description'] = focus['weather'][0]['description'].title()
        result['current_temp'] = round(focus['temp'])
        result['humidity'] = focus['humidity']
        result['cloudiness'] = focus['clouds']
        result['rain'] = str(focus['rain']['1h'])+' mmh' if focus.get('rain') else "N/A"
        result['wind'] = focus['wind_speed']
        result['current_icon'] = focus['weather'][0]['icon']
        result['daily'] = []
        for i, day in enumerate(weather['daily']):
            icon = day['weather'][0]['icon']
            max = round(day['temp']['max'])
            min= round(day['temp']['min'])
            day = datetime.strftime(datetime.fromtimestamp(day['dt']), "%A")
            result['daily'].append({'day':day ,"min": min, "max": max, "icon": icon})

        #return JsonResponse(result)

        return render(request, "weather.html", {'result': result})
