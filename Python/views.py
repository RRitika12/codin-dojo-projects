from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, "application/index.html")


def register(request):
    errors = User.objects.validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else: 
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=pw_hash )
        user = User.objects.last()
        request.session['logged_in'] = user.id
        return redirect("/dashboard")
    return redirect('/')


def login(request):
    errors = User.objects.loginValidator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else: 
        user = User.objects.get(email=request.POST['log_email'])
        request.session['logged_in'] = user.id
        return redirect('/dashboard')
    return redirect('/')


def dashboard(request):
    user = User.objects.get(id=request.session['logged_in'])
    context = {
        'user': User.objects.get(id=request.session['logged_in']),
        'all_posts': Post.objects.filter(),
    
    }
    return render(request, 'application/dashboard.html', context)


def logout(request):
    request.session['logged_in'] = None
    messages.error(request, "You have successfully logged out")
    return redirect('/')


def addpost(request):
    user = User.objects.get(id=request.session['logged_in'])
    post = Post.objects.create(description = request.POST['description'], uploader = User.objects.get(id=request.session['logged_in']))
    return redirect("/dashboard")


def posts_edit(request, my_val):
    user = User.objects.get(id=request.session['logged_in'])
    posts = Post.objects.get(id = my_val)
    context = {
        'user': User.objects.get(id=request.session['logged_in']),
        "post": Post.objects.get(id = my_val)
    }
    return render(request, "application/edit.html", context)

def process_edit(request, my_val):
    if request.method == 'POST':
        post = Post.objects.get(id = my_val)
        post.description = request.POST['description']
        post.save()
    return redirect('/dashboard')


def new(request):
    user = User.objects.get(id=request.session['logged_in'])
    context = {
        'user': User.objects.get(id=request.session['logged_in']),
    }
    return render(request, "application/new.html", context)


def destroy(request, id):
    post = Post.objects.get(id=id)
    post.delete()
    return redirect("/dashboard")

