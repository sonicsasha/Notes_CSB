from django.http.response import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from notes.models import User, Note
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.db import connection

# Create your views here.

def index(request):
    try:
        if request.session["username"]!=None:
            return HttpResponseRedirect("/notes")
        return render(request, "pages/login.html")
    except:
        return render(request, "pages/login.html")

@csrf_exempt
def signUpView(request):
    if request.method == "POST":
        if request.POST.get("username") != None and request.POST.get("password") != None:
            user=User(username=request.POST.get("username"), password=request.POST.get("password"))
            user.save()
            print("User created!")
            messages.info(request, "Account succesfully created. Please login with the credentials you entered!")
            return HttpResponseRedirect("/")
    return render(request, "pages/signup.html")

@csrf_exempt
def logInView(request):
    try:
        if request.method == "POST":
            if request.POST.get("username") != None and request.POST.get("password") != None:
                user=User.objects.filter(username=request.POST.get("username"))
                print(f"Username is: {user[0].username}")
                print(user.exists())
                if user.exists()==False and user[0].password==request.POST.get("password"):
                    print("nope")
                    messages.error(request, "User not found. Please try again!")
                    return HttpResponseRedirect("/")
                request.session["username"]=user[0].username
                return HttpResponseRedirect("/notes/")
        return render(request, "pages/login.html")
    except:
        print("Log in failed!")
        return render(request, "pages/login.html")

def notesView(request):
    print(request.session["username"])
    try:
        if request.session["username"]==None:
            return HttpResponseRedirect("/login/")
    except:
        return HttpResponseRedirect("/login/")


    notes=[]
    
    with connection.cursor() as cursor:
        for note in cursor.execute(f"SELECT note FROM notes_note WHERE user='{request.session['username']}'"):#SQL Injection
            notes.append(note[0])
    return render(request, "pages/notes.html", {"notes" : notes, "username": request.session["username"]})

def logOut(request):
    request.session["username"]=None
    return HttpResponseRedirect("/")


@csrf_exempt
def addView(request):
    #try:
    if request.session["username"]==None:
        return HttpResponseRedirect("/")
    #except:
        #return HttpResponseRedirect("/")
    
    if request.method=="POST":
        if request.POST.get("content")!=None:
            with connection.cursor() as cursor:
                cursor.execute(f"INSERT INTO notes_note (user, note) VALUES ('{request.session['username']}', '{request.POST.get('content')}')", multi=True)
        return HttpResponseRedirect("/")


