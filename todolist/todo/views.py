from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User,Item,Dolist
from datetime import datetime



def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))

    return render(request, "todo/index.html")

@login_required(login_url='/login')
def todo(request):
    user=request.user
    dolists=Dolist.objects.filter(user_todo=user)
    return render(request,"todo/todo.html",{
        "dolists":dolists
    })

@login_required(login_url='/login')
def addtodo(request):
    user=request.user
    if request.method=="POST":
        name=request.POST["name"]
        list=Dolist(user_todo=user,name_list=name)
        list.save()
        return HttpResponseRedirect(reverse("todo"))
    else:
        return render(request, "todo/addtodo.html")

@login_required(login_url='/login')
def done(request,list_id,item_id):
    if request.method == "POST":
      todo = Dolist.objects.get(pk=list_id)
      todolists=todo.item.all()
      done_item=todolists.get(id=item_id)
      if done_item.status=="C":
          done_item.status="NC"
      else:
          done_item.status = "C"
      done_item.save()
      return HttpResponseRedirect(reverse("listitem", args=(list_id,)))

@login_required(login_url='/login')
def deletetodo(request,list_id):
    todo = Dolist.objects.get(pk=list_id)
    todo.delete()
    return HttpResponseRedirect(reverse("todo"))

@login_required(login_url='/login')
def complete(request,list_id):
    todo = Dolist.objects.get(pk=list_id)
    todolists = todo.item.all().order_by('name_item')
    C = "C"
    return render(request, "todo/complete.html", {
        "todo": todo, "todolists": todolists, "C": C
    })

@login_required(login_url='/login')
def expired(request,list_id):
    todo = Dolist.objects.get(pk=list_id)
    todolists = todo.item.all().order_by('name_item')
    x= datetime.now()
    return render(request, "todo/expired.html", {
        "todo": todo, "todolists": todolists, "x": x
    })
@login_required(login_url='/login')
def listitem(request,list_id):
    todo=Dolist.objects.get(pk=list_id)
    todolists=todo.item.all().order_by('name_item')
    C="NC"

    return render(request,"todo/listitem.html",{
        "todo":todo,"todolists":todolists,"C":C
    })

@login_required(login_url='/login')
def additem(request,list_id):
    todo=Dolist.objects.get(pk=list_id)
    todolists=todo.item.all()
    if request.method=="POST":
        name=request.POST["name"]
        description=request.POST["description"]
        deadline=request.POST["deadline"]
        status = request.POST["status"]
        #x = datetime.datetime.now()
        item_=Item(name_item =name,desciption=description,deadline=deadline,status=status)
        item_.save()
        todo.item.add(item_)
        return HttpResponseRedirect(reverse("listitem", args=(list_id,)))

    return HttpResponseRedirect(reverse("index"))


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "todo/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "todo/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })
        if User.objects.filter(email=email).exists():
            return render(request, "todo/register.html", {
                "message": "Email is already taken"
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "todo/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "todo/register.html")



