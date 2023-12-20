from django.shortcuts import render,HttpResponseRedirect
from . forms import SignUPForm,LoginForm,addPostdataForm
from django.contrib.auth import authenticate,login, logout
from django.contrib import messages
from .models import Post
from django.contrib.auth.models import Group
# Create your views here.
# Home
def home(request):
    post = Post.objects.all()
    return render(request, 'blog/home.html' ,{'posts':post})

# About
def about(request):
    return render(request, 'blog/about.html')

# Contact
def contact(request):
    return render(request, 'blog/contact.html')


# Dashboard
def dashboard(request):
    if request.user.is_authenticated:
        post = Post.objects.all()
        user = request.user
        full_name = user.get_full_name()
        gps = user.groups.all()

        return render(request, 'blog/dashboard.html' , {'posts':post , 'fullName':full_name,'groups':gps})
    else:
        return HttpResponseRedirect('/login/')


# signup
def user_signup(request):
    if request.method == "POST":
        fm = SignUPForm(request.POST)
        if fm.is_valid():
            messages.success(request,"Congratullation !!! You Become an Author ")
            user = fm.save()
            group = Group.objects.get(name='Author')
            user.groups.add(group)


    else:
        fm = SignUPForm()
    return render(request, 'blog/signup.html' ,{"form" : fm})


# Logout
def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


# Login
def user_login(request):
    if not request.user.is_authenticated:
        if request.method == "POST":
            fm = LoginForm(request=request, data =request.POST)
            if fm.is_valid():
                uname  = fm.cleaned_data['username']
                upass = fm.cleaned_data['password']
                user = authenticate(username=uname, password=upass)
                if user is not None:
                    login(request,user)
                    messages.success(request,"You Logged Successfully")
                    return HttpResponseRedirect('/dashboard/')

        else:
            fm = LoginForm()
        return render(request, 'blog/login.html',{"form":fm})
    else:
        return HttpResponseRedirect('/dashboard/')

# Add post 

def add_post(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            fm = addPostdataForm(request.POST)
            if fm.is_valid():
                fm.save()
                messages.success(request,"Your post added successfully !!!")
        else:
            fm = addPostdataForm()
        return render(request,'blog/addpost.html',{"form":fm})
    else:
        return HttpResponseRedirect('/login/')

# Update  post 

def update_post(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            pi = Post.objects.get(pk=id)
            fm = addPostdataForm(request.POST,instance=pi)
            if fm.is_valid():
                fm.save()
                return HttpResponseRedirect('/dashboard/')

                
        else:
            pi = Post.objects.get(pk=id)
            fm = addPostdataForm(instance=pi)
        return render(request,'blog/updatepost.html',{"form":fm})
    else:
        return HttpResponseRedirect('/login/')


def delete_post(request,id):
    if request.user.is_authenticated:
        pi = Post.objects.get(pk=id)
        pi.delete()
        return HttpResponseRedirect('/dashboard/')
    else:
        return HttpResponseRedirect('/login/')