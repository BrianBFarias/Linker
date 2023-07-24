from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import json
from django.db import IntegrityError
from django.http import JsonResponse
import time
from django.core.serializers import serialize
from .models import User, Profile, Post

def index(request):
    return render(request, "network/index.html")

def posts(request):
    # Get start and end points
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))

    posts = Post.objects.all()

    posts = posts.order_by("-timestamp").all()

    return JsonResponse([post.serialize(request.user) for post in posts[start:end]], safe=False)


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
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


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
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
            profile = Profile(user=user)
            profile.save()

        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

@login_required
def profile(request, user_id):
    viewing_user = User.objects.get(id=user_id)
    profile_info = Profile.objects.get(user=viewing_user)
    myProfile = Profile.objects.get(user = request.user)
    posts = Post.objects.filter(creator=viewing_user)
    
    if( myProfile.following.filter(id=viewing_user.id).exists()):
        following =True
    else:
        following =False

    return render(request, "network/profile.html", {
        "profile": profile_info,
        "posts": posts,
        "following": following
    })

# API section posts---------------------------

# composing post
@login_required
def compose(request):
    if request.method == "POST":
        content = request.POST["content"]
        if content=="":
            return HttpResponseRedirect(reverse("index"))
        post = Post(creator = request.user, content = content)
        post.save()

        return HttpResponseRedirect(reverse("index"))
    
    else:
        return JsonResponse({"error": "POST request required."}, status=400)


# obtain singular post
@csrf_exempt
@login_required
def like(request, post_id):        
    post = Post.objects.get(id = post_id)
    user_profile = Profile.objects.get(user = request.user)
    if user_profile in post.likes.all():
        # The user is in the likes list
        post.likes.remove(user_profile)
    else:
        # The user is not in the likes list
        post.likes.add(user_profile)

    return JsonResponse(post.serialize(request.user), safe=False)


# find post and return its data
def post(request, post_id):        
    post = Post.objects.get(id = post_id)
    return JsonResponse(post.serialize(request.user), safe=False)

# saving edited post
@csrf_exempt
def save(request, post_id):
    if request.method != "POST":
        return JsonResponse({"error": "POST request required."}, status=400)
    
    post = Post.objects.get(id = post_id)
    data = json.loads(request.body)
    content = data.get("content", "")

    post.content = content
    post.save()
    return JsonResponse(post.serialize(request.user), safe=False)

    
def prof_posts(request):
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))

    posts = Post.objects.filter(creator = request.user)[start:end]

    return JsonResponse([post.serialize(request.user) for post in posts], safe=False)

# follow/unfollow actions
def follow(request, user_id):
    my_profile = Profile.objects.get(user = request.user)
    viewing_user = User.objects.get(id = user_id)
    viewing_profile = Profile.objects.get(user = viewing_user)

    # if is following right now
    if my_profile.following.filter(pk=viewing_user.pk).exists():
        print('follow')
        my_profile.following.remove(viewing_user)
        my_profile.save()

        viewing_profile.followers.remove(request.user)
        viewing_profile.save()
        data = {
        "following": False,
        "followers": viewing_profile.followers.count()
        }

    
    # not following right now
    else:
        print('follow')
        my_profile.following.add(viewing_user)
        my_profile.save()

        viewing_profile.followers.add(request.user)
        viewing_profile.save()
        data = {
            "following": True,
            "followers": viewing_profile.followers.count()
        }

    return JsonResponse(data, safe=False)


def following_posts(request):
    # Get start and end points

    profile = Profile.objects.get(user = request.user)
    
    start = int(request.GET.get("start") or 0)
    end = int(request.GET.get("end") or (start + 9))

    posts = []

    for user in profile.following.all():
        for post in Post.objects.filter(creator = user).order_by("-timestamp"):   
            posts.append(post)

    posts = sorted(posts, key=lambda post: post.timestamp, reverse=True)
    print(posts)
    return JsonResponse([post.serialize(request.user) for post in posts[start:end]], safe=False)


def following(request):
    return render(request, "network/following.html")