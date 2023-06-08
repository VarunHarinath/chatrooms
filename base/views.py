from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from .models import Room,Topic
from .forms import RoomForm
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.

def loginPage(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        try:
            user = User.objects.get(username= username)
            # return redirect('home')
        except:
            messages.error(request,'User Does ot exsist')

        user = authenticate(request,username=username,password=password)

        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'Username or password does not exsist')
        
    return render(request,'base/login_register.html')



def UserLogout(request):
    logout(request)
    return redirect('home')


rooms = [
    {'id':1,'name':"Movies"},
    {'id':2,'name':"Technology"},
    {'id':3,'name':"Sports"},
    {'id':4,'name':"Songs"},
]


def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    rooms = Room.objects.filter(Q(topic__name__icontains=q) | Q(name__icontains=q) | Q(descrption__icontains=q))
    topic = Topic.objects.all()
    room_count = rooms.count()
    return render(request,'base/home.html',{'rooms':rooms,'topics':topic,'room_count':room_count})

def room(request,pk):
    room = Room.objects.get(id=pk)
    return render(request,'base/room.html',{'room':room})

# @login_required(login_required='/login')
def CreateRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid:
            form.save()
            return redirect('home')

    context = {'form':form}
    return render(request,'base/room_forum.html',context)



def updateRoom(request,pk):
    room = Room.objects.get(id=pk)
    form = RoomForm(instance=room)
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid:
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'base/room_forum.html',context)


def deleteRoom(request,pk):
    room = Room.objects.get(id=pk)
    if request.method == "POST":
        room.delete()
        return redirect('home')
    
    return render(request,'base/delete.html',{'obj':room})



