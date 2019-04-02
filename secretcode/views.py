from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.template import loader
import os
import random
from django.conf import settings
from .models import User
from django.views.decorators.csrf import csrf_exempt

#landing page server
def home(request):
	return render(request, 'home.html')

#insecure login functionality below
@csrf_exempt #exempt CSRF protection to make this vulnerable
def secret(request):
    number = random.randint(1,8000)
    if request.method == "POST":
    	print("THR")
    	print(request)
    	username = request.POST.get("name")
    	password = request.POST.get("passwd")
    	if username == 'admin':
    		me = User.objects.get(username = username)
    	else:
    		return render(request, 'home.html')
    	#very insecure manual login functionality, allows unlimited password attempts
    	if password == me.password:
            template = loader.get_template('secret.html')
            me.secret = number
            context = {'secret': me.secret}
            return HttpResponse(template.render(context, request))
    	else:
    		return render(request, 'home.html')
    else:
    	return render(request, 'home.html')






