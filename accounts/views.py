from django.shortcuts import render
from django.contrib.auth import views as auth_views
from accounts.forms import SignupForm
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect
import json

from accounts.models import User


def AjaxloginView(request):
    email= request.POST.get('email')
    password = request.POST.get('password')
    user = authenticate(email=email, password=password)
    if user is not None:
        if user.is_active:
            login(request, user)
            return HttpResponse(json.dumps({"message": "Success"}),content_type="application/json")
        else:
            return HttpResponse(json.dumps({"message": "inactive"}), content_type="application/json")
    else:
        return HttpResponse(json.dumps({"message": "invalid"}),content_type="application/json")
    return HttpResponse(json.dumps({"message": "denied"}),content_type="application/json")


# Create your views here.
def SignupAjaxView(request):
	if request.method == 'POST':
		fname = request.POST.get('first_name')
		lname = request.POST.get('last_name')
		email = request.POST.get('email')
		password1 = request.POST.get('password1')
		password2 = request.POST.get('password2')
		data = {'first_name':fname, 'last_name':lname, 'email':email, 'password2':password2, 'password1':password1}
		form = SignUpForm(data = data)
		if form.is_valid():
			user = form.save(commit=False)
			user.is_active = True
			user.save()
			return HttpResponse(json.dumps({"message": "Success"}),content_type="application/json")
		else:
			return HttpResponse(json.dumps({"message":form.errors}),content_type="application/json")
	else:
		form = SignUpForm()
	return HttpResponse(json.dumps({"message": "Denied"}),content_type="application/json")