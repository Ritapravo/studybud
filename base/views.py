from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.db.models import Q
from .models import Room, Topic
from .forms import RoomForm
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
    q = request.GET.get('q')
    if(q==None):
        q = ''
    print(q)
    rooms = Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(name__icontains=q) |
        Q(description__icontains=q) 
    )
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms': rooms, 'topics': topics, 'room_count':room_count}
    return render (request, 'base/home.html', context)

def room(request, pk):
    # return HttpResponse('Room Page')
    room = Room.objects.get(id=pk)
    context = {'room': room}
    return render (request, 'base/room.html', context)

def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if(form.is_valid()):
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)

    if(request.method=='POST'):
        form = RoomForm(request.POST, instance=room)
        if(form.is_valid()):
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'base/room_form.html', context)

def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if(request.method=='POST'):
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})
