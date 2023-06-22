from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def home(request):
    # request object is going to be the http object. It tells us about the 
    # what kind of request is sent, what kind of data is passed in, whats the user sending to the bckend
    # return HttpResponse('Home Page')
    return render (request, 'home.html')
def room(request):
    # return HttpResponse('Room Page')
    return render (request, 'room.html')