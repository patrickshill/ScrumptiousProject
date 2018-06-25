from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "scrumptious/index.html")

def register(request):
    return render(request, "scrumptious/register.html")

def registerUser(request):
    return redirect("/")