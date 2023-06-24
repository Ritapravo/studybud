from django.shortcuts import render
from django.http import HttpResponse
from .models import Room
# Create your views here.

# rooms = [
#     {'id':1, 'name': 'lets learn python'}, 
#     {'id':2, 'name': 'Design with me'},
#     {'id':3, 'name': 'Frontend developers'},
# ]

def home(request):
    # request object is going to be the http object. It tells us about the 
    # what kind of request is sent, what kind of data is passed in, whats the user sending to the bckend
    # return HttpResponse('Home Page')
    rooms = Room.objects.all()
    context = {'rooms': rooms}
    return render (request, 'base/home.html', context)

def room(request, pk):
    # return HttpResponse('Room Page')
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render (request, 'base/room.html', context)