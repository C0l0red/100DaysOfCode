from django.shortcuts import render
from django.core.mail import send_mail
from django.http import JsonResponse
from .forms import SendEmail 
from django_emailsender.settings import EMAIL_HOST_USER, EMAIL_HOST_PASSWORD

# Create your views here.
def send(request):
    sub = SendEmail()
    if request.method == 'POST':
        sub = SendEmail(request.POST)
        print(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
        subject = str(sub['subject'].value())
        message = str(sub['message'].value())
        recepient = str(sub['recepient'].value())
        send_mail(subject, 
            message, EMAIL_HOST_USER, [recepient], fail_silently = False)
        return render(request, 'success.html', {'recepient': recepient})
    return render(request, 'index.html', {'form':sub})