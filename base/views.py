from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Room, Topic, Message
from .forms import RoomForm, UserForm

# Create your views here.

# rooms = [
#     {'id':1, 'name': 'lets learn python'}, 
#     {'id':2, 'name': 'Design with me'},
#     {'id':3, 'name': 'Frontend developers'},
# ]

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated :
        return redirect ('home')

    if(request.method == 'POST'):
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
        user = authenticate(request, username=username, password=password)

        if(user is not None):
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')
    context = {'page':page}
    return render(request, 'base/login_register.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

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
    topics = Topic.objects.all()[0:5]
    room_count = rooms.count()
    room_messages = Message.objects.filter(Q(room__topic__name__icontains=q))
    context = {'rooms': rooms, 'topics': topics, 
               'room_count':room_count, 'room_messages':room_messages}
    return render (request, 'base/home.html', context)

def registerPage(request):
    page ='register'
    form = UserCreationForm()

    if(request.method=='POST'):
        form = UserCreationForm(request.POST)
        if(form.is_valid()):
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration')

    context = {'page':page, 'form':form}
    return render(request, 'base/login_register.html', context)

def room(request, pk):
    # return HttpResponse('Room Page')
    room = Room.objects.get(id=pk)
    room_messages = room.message_set.all()#.order_by('-created')
    participants = room.participants.all()

    if(request.method=='POST'):
        print("request = ",request)
        message = Message.objects.create(
            user=request.user, 
            room=room,
            body=request.POST.get('body')
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {'room': room, 'room_messages':room_messages, 
               'participants':participants}
    return render (request, 'base/room.html', context)


def userProfile(request, pk):
    user = User.objects.get(id=pk)
    rooms = user.room_set.all() # what is this room_set ?
    room_messages = user.message_set.all() # what is this message_set ?
    topics = Topic.objects.all()
    context = {'user':user, 'rooms':rooms, 
               'room_messages':room_messages, 'topics':topics}
    return render(request, 'base/profile.html', context)


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    topics = Topic.objects.all()
    if request.method == 'POST':
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        Room.objects.create(
            host = request.user,
            topic = topic, 
            name = request.POST.get('name'),
            description = request.POST.get('description')
        )
        return redirect('home')
        # form = RoomForm(request.POST)
        # if(form.is_valid()):
        #     room = form.save(commit=False) #what does this commit=False do?
        #     room.host = request.user
        #     room.save()
        #     return redirect('home')

    context = {'form': form, 'topics':topics}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def updateRoom(request, pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance = room)
    topics = Topic.objects.all()
    if(request.user != room.host):
        return HttpResponse('You are not allowed here')

    if(request.method=='POST'):
        topic_name = request.POST.get('topic')
        topic, created = Topic.objects.get_or_create(name=topic_name)
        room.name = request.POST.get('name')
        room.topic = topic
        room.description = request.POST.get('description')
        room.save()
        return redirect('home')
        # form = RoomForm(request.POST, instance=room)
        # if(form.is_valid()):
        #     form.save() 
        #     return redirect('home')

    context = {'form': form, 'topics':topics, 'room':room}
    return render(request, 'base/room_form.html', context)

@login_required(login_url='login')
def deleteRoom(request, pk):
    room = Room.objects.get(id=pk)
    if(request.method=='POST'):
        room.delete()
        return redirect('home')
    return render(request, 'base/delete.html', {'obj':room})

@login_required(login_url='login')
def deleteMessage(request, pk):
    message = Message.objects.get(id=pk)

    if request.user != message.user:
        return HttpResponse('You are not allowed here!')

    if(request.method=='POST'):
        message.delete()
        return redirect('home' )
    
    return render(request, 'base/delete.html', {'obj':message})

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if(request.method=='POST'):
        form = UserForm(request.POST, instance=user)
        if(form.is_valid()):
            form.save()
            return redirect('user-profile', pk=user.id)

    context = {'form':form}
    return render (request, 'base/update-user.html', context)

def topicPage(request):
    q = request.GET.get('q')
    if(q==None):
        q = ''
    topics = Topic.objects.filter(name__icontains=q) # what is this name__icontains thing ??
    context = {'topics':topics}

    return render(request, 'base/topics.html', context)

def activitiesPage(request):
    room_messages = Message.objects.all()
    context = {'room_messages':room_messages}
    return render(request, 'base/activity.html', context)