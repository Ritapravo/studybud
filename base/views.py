from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

rooms = [
    {'id':1, 'name': 'lets learn python'}, 
    {'id':2, 'name': 'Design with me'},
    {'id':3, 'name': 'Frontend developers'},
]

def home(request):
    # request object is going to be the http object. It tells us about the 
    # what kind of request is sent, what kind of data is passed in, whats the user sending to the bckend
    # return HttpResponse('Home Page')
    context = {'rooms': rooms}
    return render (request, 'base/home.html', context)
def room(request):
    # return HttpResponse('Room Page')
    return render (request, 'base/room.html')