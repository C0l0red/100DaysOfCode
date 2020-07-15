from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
import requests
from datetime import datetime
from pprint import pprint
from django.contrib import messages


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
    country = geocode['standard']['countryname']
    return city, country, geocode['latt'], geocode['longt']

#weather = get_weather(*geocoder("Abuja, Nigeria"))

def hourly(dt):
    hr, suffix = int(dt.strftime("%I")), dt.strftime("%p")
    rep = f"{hr}{suffix}"
    hours = {}
    for hour in range(24):
        hours.update({rep: hour})
        if hr != 12:
            hr += 1
        else:
            hr = 1
            suffix = "PM" if suffix == "AM" else "AM"
        rep = f"{hr}{suffix}"
    return hours

# Create your views here.
def home(request):
    if any(x not in request.session for x in ["city", 'country', 'weather']):
        city, country, *GEOCODE = geocoder("Abuja, Nigeria")
        request.session['weather'] = get_weather(*GEOCODE)
        request.session['city'] = city
        request.session['country'] = country

    weather = request.session['weather']
    city = request.session['city']
    country = request.session['country']

    if 'hour' not in request.GET:
        focus = weather['current']
    else:
        index = request.session.get('hourly')[request.GET['hour']]
        focus = weather['hourly'][index]

    if request.method == "POST":
        location= request.POST['location']
        try:
            city, country, *GEOCODE = geocoder(location)
            weather = get_weather(*GEOCODE)
        except:
            messages.add_message(request, messages.ERROR, "Unable to get weather data. Try again or change input.")
        else:
            request.session['weather'] = weather
            request.session['city'] = city
            request.session['country'] = country
            request.session.pop('hourly')
        finally:
            return HttpResponseRedirect('/weather/')

    if request.method == "GET":
        dt =  weather['timezone_offset'] + focus['dt']
        dt = datetime.fromtimestamp(dt)
        print(weather['timezone_offset'], focus['dt'])

        hrs = int(dt.strftime("%H")) 
        hrs = hrs - 12 if hrs >= 20 else hrs + 12 if hrs < 8 else hrs
        
        progress =round( ( (( (hrs * 60) + int(dt.strftime("%M") )) - 480) / 720 ) * 100, 2)

        if not request.session.get('hourly'):
            request.session['hourly'] = hourly(dt)

        result = {}
        result['time'] = dt.strftime( "%a, %I:%M %p")
        if int(dt.strftime("%H")) in range(8, 20):
            result['con'], result['rev'] = "AM", "PM"
        else:
            result['con'], result['rev'] = "PM", "AM"
        result['current_hour'] = dt.strftime("%I%p")
        result['current_hour'] = result['current_hour'][1:] if result['current_hour'].startswith('0') else result['current_hour']
        result['hours'] = request.session['hourly'].keys()
        result['progress'] = progress
        result['city'] = city
        result['country'] = country
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


        return render(request, "weather.html", {'result': result})
