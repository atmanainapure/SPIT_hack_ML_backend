from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.http import HttpResponse
# This code imports the login_required decorator which is used to require a user to be logged in to access a view.
from django.contrib.auth.decorators import login_required
from .models import Profile, FollowersCount, Syllabus, Assignment
from itertools import chain
import random

# Create your views here.



def syllabus(request):
    print("chal raha hai")
    import cv2
    import pytesseract
    import re
    import requests
    from bs4 import BeautifulSoup


    pytesseract.pytesseract.tesseract_cmd = 'C:/Program Files/Tesseract-OCR/tesseract.exe'
    # Load the image
    image = cv2.imread('"C:\SPIT_Memoirs\spit-hackthon-remain\StudyPat\media\syllabus_images\syllabus1.png"')

    # Convert the image to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    def isblank(s):
        return True if len(s)>0 else False
    # Apply OCR using pytesseract
    text = pytesseract.image_to_string(gray)
    #cleaning the text
    text=text.replace("Title"," ")
    text=text.split("\n")
    text=[s for s in text if not (s.isdigit() or s.isalpha() or s.isspace() or s.isalnum())]

    text=[s for s in text if (isblank(s))]
    return render(request,'syll-aasign.html',{'data':text})


#================================================================================================

def landing(request):
    return render(request, 'landing.html')

@login_required(login_url='signin')
def index(request):

    #We sent user profile and posts as a key value pair because we wanted to show it on the front end hence we sent it to the template.
    return render(request, 'index.html')

@login_required(login_url='signin')
def upload_s(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')

        #This code creates a new post with the given user, image, and caption, then saves it.
        new_post = Syllabus.objects.create(user=user, image=image)
        new_post.save()

    return redirect('/syllabus_home')

@login_required(login_url='signin')
def upload_a(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')

        #This code creates a new post with the given user, image, and caption, then saves it.
        new_post = Assignment.objects.create(user=user, image=image)
        new_post.save()

    return redirect('/syllabus_home')

@login_required(login_url='signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        # whatever we write in the button of "search for username", it fetches that info here by selecting the name of the button
        username = request.POST['username']
        #Heart of search function. icontains searchs for the substring that we are searching for in every entry.
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})

@login_required(login_url='signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')

    post = Post.objects.get(id=post_id)

    #This code filters the LikePost objects to find the first instance with a matching post_id and username.
    like_filter = LikePost.objects.filter(post_id=post_id, username=username).first()

    if like_filter is None:
        new_like = LikePost.objects.create(post_id=post_id, username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
    #If the user has already liked the post, he/she should be able to unlike the post, hence the else statement.
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
    post.save()
    return redirect('/home')

@login_required(login_url='signin') 
def profile(request, pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_post_length = len(user_posts)

    follower = request.user.username
    user = pk

    if FollowersCount.objects.filter(follower=follower, user=user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'
    #We want to make a feed for the user. Hence we make it by storing all the posts which the user's following has posted.
    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following = len(FollowersCount.objects.filter(follower=pk))
    #this is the context dictionary that we can normally send to the template for it to do operations.
    context = {
        'user_object': user_object,
        'user_profile': user_profile,
        'user_posts': user_posts,
        'user_post_length': user_post_length,
        'button_text': button_text,
        'user_followers': user_followers,
        'user_following': user_following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='signin')
def follow(request):
    if request.method == 'POST':
        #the key used here is given in the 'name' attribute in the template. 
        follower = request.POST['follower']
        user = request.POST['user']
        #If the user has clicked on the follow button but an object of followercount already exists, this means the user is trying to unfollow the user in question.
        if FollowersCount.objects.filter(follower=follower, user=user).first():
            delete_follower = FollowersCount.objects.get(follower=follower, user=user)
            delete_follower.delete()
            
        #If the user has clicked on the follow button but an object of followercount doesnt not  exist, this means the user is trying to follow the user in question.
        else:
            new_follower = FollowersCount.objects.create(follower=follower, user=user)
            new_follower.save()
        return redirect('/profile/'+user)
    else:
        return redirect('/home')

@login_required(login_url='signin')
def settings(request):
    #We fetch the user profile
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        #In Django, the request.FILES attribute is a dictionary-like object that is used to access uploaded files
        if request.FILES.get('image') is None:
            #None signifies that the user hasn't uploaded anything. Hence we fethc the image from the model.
            image = user_profile.profileimg
            #This code is retrieving the user's bio from a POST request and assigning it to the variable "bio".
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()

        return redirect('settings')
    return render(request, 'setting.html', {'user_profile': user_profile})

def signup(request):

    #This code is retrieving the username, email, and passwords from a POST request and storing them in variables.
    if request.method == 'POST':
        #we are accessing it with css selectors. (using the name)
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            #Checks if the given email already exists in the User database, and if so, displays an error message and redirects the user.
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                #This code creates a new user with the given username, email and password, and then saves the user.
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()

                #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)

                #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                #We create the profile object by extracting the username from the user builtin model
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request, "The passwords don't match!")
            return redirect('signup')
        
    else:
        return render(request, 'signup.html')

def signin(request):
    
    if request.method    == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        #This code authenticates the user by verifying the username and password provided.
        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('/home')#We are redirected to the home page
        else:
            messages.info(request, 'Credentials Invalid')
            return redirect('signin')

    else:
        return render(request, 'signin.html')

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url='signin')
def syllabus_home(request):
    return render(request, 'syll-aasign.html')


@login_required(login_url='signin')
def index_tensor(request):
    return render(request, 'index_tensor.html')