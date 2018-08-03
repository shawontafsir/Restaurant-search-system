from django.contrib.auth import authenticate
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, render_to_response, redirect
from django.core.urlresolvers import reverse

from register.forms import RegistrationForm, loginForm
from register.models import Register
from restaurant.models import Restaurant

def logout(request):
    form = loginForm(request.POST or None)
    try:
        del request.session['username']
    except:
        pass
    return HttpResponseRedirect("/register/login")
    #return render(request, 'register/login.html', {'form': form,'is_valid':False, 'user':None})

def login(request):
    form = loginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        try:
            user = Register.objects.get(name=username,password=password)
            request.session['username'] = user.name
        except:
            user = None
            request.session['username'] = None
        if user:
            return HttpResponseRedirect('/restaurant/')
        else:
            return render(request, 'register/login.html', {'form': form, 'is_valid': False, 'error_message': 'Invalid login', 'user': None})
        #user = authenticate(username=user.name, password=user.password)
    return render(request, 'register/login.html',{'form': form,'is_valid':False, 'user':None})

def register(request):
    form = RegistrationForm(request.POST or None)
    if form.is_valid():
        user = Register()
        user.name = form.cleaned_data['username']
        user.mobileNo = form.cleaned_data['mobileNo']
        user.password = form.cleaned_data['password1']
        user.email = form.cleaned_data['email']
        user.save()
        request.session['username'] = user.name

        return HttpResponseRedirect('/restaurant/')
    return render(request, 'register/signUp.html', {'form': form})

def profile(request):
    user = Register.objects.get(name=request.session.get('username'))
    return render(request, 'register/profile.html', {'is_valid':True, 'user':user})