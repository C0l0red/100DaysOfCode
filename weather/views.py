from django.shortcuts import render
from django.http import HttpResponseRedirect, JsonResponse
import requests
from datetime import datetime, timedelta
from pprint import pprint
from django.contrib import messages
from time import time

"""
This makes the call to OpenWeatherMap API with latitude and longitude coordinates
The return value is a dictionary
"""
def get_weather(lat, lon, exclude='', unit='metric'):
    url = 'https://api.openweathermap.org/data/2.5/onecall'
    params = {'lat': lat, 'lon': lon, 'exclude': exclude,
             'appid': '9f89938697ac4339dfc5ef3bac378dda', "units": unit,
             'time': time()}
    weather = requests.get(url, params)
    return weather.json()

"""
This makes a call to OpenCageData API to geocode the written location passed by the client into longitude and latitude coordinates
to be passed into the OpenWeatherMap API call.
It also returns the city and country names to be used as labels in the template
"""
def geocoder(location):
    url = 'https://geocode.xyz'
    params = {"locate": location, 'geoit':"JSON"}
    r = requests.get(url, params)
    geocode = r.json()
    city = geocode['standard']['city']
    country = geocode['standard']['countryname']
    return city, country, geocode['latt'], geocode['longt']

"""
This function returns a dictionary mapping each hour to it's index in the 'hourly' array returned from the OpenWeatherMap API call
"""
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

    """
    This block of code is run when a POST request is made. It checks for the location in the form and calls the OpenWeatherMap API
    in a try/except/else/finally block, this is to ensure that the web app doesn't crash with incorrect or unidentifiable location entries.
    Should there be an error, a message will be passed to the  client which will be displayed as an alert.
    If there's no exception, then the sessions are replaced with the new values from the API call.
    """
    if request.method == "POST":
        print("post")
        location= request.POST['location']
        try:
            city, country, *GEOCODE = geocoder(location)
            weather = get_weather(*GEOCODE)
        except:
            messages.add_message(request, messages.ERROR, "Unable to get weather data. Try again or change input.")
        else:
            request.session.clear()
            request.session['weather'] = weather
            request.session['city'] = city
            request.session['country'] = country
            request.session['refresh'] = int(time()) + timedelta(minutes=1).seconds
            request.session['coordinates'] = GEOCODE
            request.session.pop('hourly')
        finally:
            return HttpResponseRedirect('/weather/')


    #This checks if the required sessions neccessary already exist, if not, they're all refreshed to Abuja, Nigeria
    if any(x not in request.session for x in ["city", 'country', 'weather', 'refresh', 'coordinates']):
        request.session.clear()
        city, country, *GEOCODE = geocoder("Abuja, Nigeria")
        request.session['weather'] = get_weather(*GEOCODE)
        request.session['city'] = city
        request.session['country'] = country
        request.session['coordinates'] = GEOCODE
        request.session['refresh'] = int(time()) + timedelta(minutes=1).seconds


    if request.session['refresh'] < int(time()):
        request.session['weather'] = get_weather(*request.session['coordinates'])
        request.session['refresh'] = int(time()) + timedelta(minutes=1).seconds


    weather = request.session['weather']
    city = request.session['city']
    country = request.session['country']

    #This checks if 'hour' is in the URL params, if it is, then it changes focus from the current hour of the location in question
    #to the specific hour the user wants to view
    if 'hour' not in request.GET:
        focus = weather['current']
    else:
        index = request.session.get('hourly')[request.GET['hour']]
        focus = weather['hourly'][index]
        

    """
    In the event of a GET request, a 'result' dictionary is used to get data from the current 'weather' session stored and scrapes
    useful data to be sent to the template
    """
    if request.method == "GET":
        dt =  weather['timezone_offset'] + focus['dt']
        dt = datetime.fromtimestamp(dt)

        #This block of code calculates the percentage to be displayed on the progress bar in the template as per the current time
        hrs = int(dt.strftime("%H")) 
        hrs = hrs - 12 if hrs >= 20 else hrs + 12 if hrs < 8 else hrs
        progress =round( ( (( (hrs * 60) + int(dt.strftime("%M") )) - 480) / 720 ) * 100, 2)

        #This check for the 'hourly' session, a session used to store the hours as keys in a dictionary where the value points to 
        #the index of the hour in the hourly array returned from the OpenWeatherMap API
        if not request.session.get('hourly'):
            request.session['hourly'] = hourly(dt)

        #This creates the result dictionary to be sent to the template and populates it using sessions
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

        #This iterates through the 'daily' array returned from the OpenWeatherMap API call to be displayed as days in the template
        #They are stored in the 'daily' key of the 'result' dictionary 
        for i, day in enumerate(weather['daily']):
            icon = day['weather'][0]['icon']
            max_ = round(day['temp']['max'])
            min_ = round(day['temp']['min'])
            day = datetime.strftime(datetime.fromtimestamp(day['dt']), "%A")
            result['daily'].append({'day':day ,"min": min_, "max": max_, "icon": icon})


        return render(request, "weather.html", {'result': result})
