from django.shortcuts import render, redirect
from .models import *
from django.contrib import messages
import bcrypt

def index(request):
    return render(request, 'index.html')

def register(request):
    #Check if Post request
    if request.method == "POST":
        #Check if register object is valid
        errors = User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/')

        #Check to see if user email is already in use
        user = User.objects.filter(email=request.POST['email'])
        if len(user) > 0:
            messages.error(request, "Email is already in use.", extra_tags="email")
            return redirect('/')

        #Hash the password with bcrypt
        pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()

        #Create user in database
        User.objects.create(
            first_name=request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = pw
        )

        #Put user Id into session and redirect
        request.session['user_id'] = User.objects.last().id 
        return redirect('/quotes')
    else:
        return redirect('/')

def login(request):
    #check if POST REQUEST
    if request.method == "POST":
        #Validate the login object
        errors = User.objects.login_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags = key)
            return redirect('/')

        user = User.objects.filter(email=request.POST['login_email'])
        if len(user) == 0:
            messages.error(request, "Invalid Email/Pasword", extra_tags = "login")
            return redirect('/')
        
        if not bcrypt.checkpw(request.POST['login_password'].encode(),user[0].password.encode()):
            messages.error(request, "Invalid Email/Password", extra_tags = "login")
            return redirect('/')

        request.session['user_id'] = user[0].id 
        return redirect('/quotes')
    else:
        return redirect('/')

def quotes (request):
    if 'user_id' not in request.session:
        return redirect('/')
    else:
        context = {
            'user': User.objects.get(id=request.session['user_id']),
            'all_quotes': Quote.objects.all()
        }
        return render(request, 'quotes.html', context)

def logout(request):
    if 'user_id' in request.session:
        del request.session['user_id']
    return redirect('/')

def create_quote(request):
    if request.method == "POST":
        errors = Quote.objects.quote_validator(request.POST)
        if len(errors)> 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/quotes')
        
        Quote.objects.create(
            author = request.POST['author'],
            quote = request.POST['quote'],
            user=User.objects.get(id=request.session['user_id'])
        )
        return redirect('/quotes')
    else:
        return redirect('/logout')

def delete_quote(request, quote_id):
    delete = Quote.objects.get(id = quote_id)
    delete.delete()
    return redirect('/quotes')

def edit_user(request):
    context = {
        'edit': User.objects.get(id=request.session['user_id']),
    }
    return render(request, 'edit_user.html', context)

def update_user(request):
    if request.method == "POST":
        errors = User.objects.edit_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value, extra_tags=key)
            return redirect('/edit_user')
        user = User.objects.filter(email=request.POST['edit_email'])
        if len(user) > 0:
            messages.error(request, "Email is already in use.", extra_tags="edit_email")
            return redirect('/edit_user')
        update = User.objects.get(id=request.session['user_id'])
        update.first_name = request.POST['edit_first_name']
        update.last_name = request.POST['edit_last_name']
        update.email = request.POST['edit_email']
        update.save()
        return redirect('/quotes')
    else:
        return redirect('/logout')

def show_user(request, user_id):
    context = {
        'user': User.objects.get(id=user_id) 
    }
    return render(request, 'show_user.html', context)

def like(request, quote_id, user_id):
    quo = Quote.objects.get(id = quote_id)
    user = User.objects.get(id = user_id)

    quo.likes.add(user)
    return redirect('/quotes')