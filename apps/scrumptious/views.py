from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

#Page views
def index(request):
    return render(request, "scrumptious/index.html")

def register(request):
    return render(request, "scrumptious/register.html")

def login(request):
    return render(request, "scrumptious/login.html")

def projects(request):
    return HttpResponse("User projects page")


#Actions
def registerUser(request):
    return HttpResponse("Successful registration")

def loginUser(request):
    return redirect("/projects")