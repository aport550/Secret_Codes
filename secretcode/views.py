from django.shortcuts import render
from django.http import HttpResponse
from django.http import Http404
from django.template import loader
import os
import random
from django.conf import settings
from .models import User
from .models import Hint
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.template import RequestContext

#Security Vulnerabilities- 1) Unlimited Password attempts- Brute Force Vulnerable 
                         # 2) XSS Vulnerability- on homepage if user clicks "CLICK FOR PASSWORD BUTTON" 
                         #    It will take the hint entry from the last user submitted post and set it to the value of the button
                         #    which if  JS will execute on users browser
                         # 3) allows for much too long username/pass size
                          
#landing page server
def home(request):
	#myCookie = request.COOKIE['cookie_name']
    try:
        hints = Hint.objects.all()
        length = len(Hint.objects.all())
        print(length)
        hint = Hint.objects.all()[length-1]
        template = loader.get_template('home.html')
        context = {'hint': hint}
        return HttpResponse(template.render(context, request))
    except:
        return render(request, 'home.html')

def signup(request):
    return render(request, 'signup.html')

#insecure- can type in as many characters as you want- can cause overflow
def createUser(user,psswd,sct):
    new_user = User.objects.create(username = user, password = psswd, secret = sct)
    return new_user

def createHint(username,hint):
    new_hint = Hint.objects.create(username = username, hint = hint)
    return new_hint

def reg(request):
    if request.method == "POST":
        createUser(request.POST.get("name"), request.POST.get("password"), request.POST.get("secret"))
        messages.success(request, 'Your account was created! Your secret is safe with us!')
        return render(request, 'home.html')
    else:
        return render(request, 'home.html')


#insecure login functionality below- allows unlimited password attempts
#Hard to cause SQLIs and XSS since django automatically escapes input

def getaccess(request):
	try:
	    myCookies = request.COOKIES
	    secret = myCookies['password']
	    username = myCookies['username']
	    template = loader.get_template('secret.html')
	    context = {'secret': username + "s password for this site is " + secret}
	    return HttpResponse(template.render(context, request))
	except:
		pass

def hints(request):
    if request.method == "POST":
        createHint(request.POST.get("username"), request.POST.get("hint"))
        return render(request, 'home.html')
    else:
        return render(request, 'home.html')

@csrf_exempt #try to exempt CSRF protection
def secret(request):
    number = random.randint(1,8000)
    if request.method == "POST":
        username = request.POST.get("name")
        password = request.POST.get("passwd")
        flag = False
        verified = User.objects.all()
        for u in verified:
            if username == u.username:
                flag = True
        if flag == True:
            me = User.objects.get(username = username)
            if password == me.password:
                template = loader.get_template('secret.html')
                context = {'secret': me.secret}
                response = HttpResponse(template.render(context, request))
                response.set_cookie('username', username, 3600)
                response.set_cookie('password', password, 3600)
                #response.set_cookie('secret', me.secret, 3600)
                return response
            else:
                template = loader.get_template('home.html')
                context = {'username': username}
                return HttpResponse(template.render(context, request))
        else:
            template = loader.get_template('home.html')
            context = {'username': username}
            return HttpResponse(template.render(context, request))

        #insecure login functionality- allows unlimited password attempts
    else:
        return render(request, 'home.html')


