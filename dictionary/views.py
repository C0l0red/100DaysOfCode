from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponseRedirect
import requests
from django_dictionary.settings import API_KEY

def get_word(word):
    url = f"https://wordsapiv1.p.rapidapi.com/words/{word}"
    print(API_KEY) 
    headers = {
        'x-rapidapi-host': "wordsapiv1.p.rapidapi.com",
        'x-rapidapi-key': API_KEY
        }
    r = requests.get(url, headers=headers)
    #print(r.json())
    return r.json()


# Create your views here.
def dictionary(request, word=None):
    if request.GET.get('word'):
        return redirect("dictionary", word= request.GET['word'])

    if word:
        request.session["result"] = get_word(word)

    if "result" not in request.session:
        request.session['result'] = get_word('example')

    result = request.session['result']
    

    return render(request, 'dictionary.html' , {'Result': result})
    #return JsonResponse(result)
