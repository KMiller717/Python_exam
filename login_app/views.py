
# Create your views here.
from django.shortcuts import render, redirect
from .models import User
from django.contrib import messages
import bcrypt
from django.contrib.sessions.models import Session


def index(request):  
    return render(request, 'index.html')


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    
    else:
        pw_hash= bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        print(pw_hash)

        User.objects.create(
            email = request.POST['email'],
            first_name=request.POST['first_name'],
            last_name = request.POST['last_name'],
            password = pw_hash
        )    
        messages.error(request, "Created account, please log in to verify account")
    return redirect('/')

def login(request):
    users = User.objects.filter(email = request.POST['email'])
    
    if len(users) != 1:
        messages.error(request, 'No user with email in the database')
        return redirect('/')
    
    user = users[0]
    print(user.first_name)
    if not bcrypt.checkpw(request.POST['password'].encode(), user.password.encode()):
        messages.error(request, "Password does not match")
        return redirect('/')

    session = request.session
    session['user_email'] = user.email
    session['user_first_name'] = user.first_name
    session['user_last_name'] = user.last_name
    session['user_id'] = user.id
    session.save()
    
    return redirect('/job')  
# The above line's redirect needs to change   


def logout(request):
    del(request.session['user_first_name'])
    del(request.session['user_email'])
    del(request.session['user_id'])
    del(request.session['user_last_name'])    
    return redirect('/')