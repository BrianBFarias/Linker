
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("profile/<int:user_id>", views.profile, name="profile"),
    path("following", views.following, name="following"),


    # API Routes
    path("compose", views.compose, name="compose"),
    path("posts", views.posts, name="posts"),
    path("following_posts", views.following_posts, name="following_posts"),
    path("save/<int:post_id>", views.save, name="save"),
    path("like/<int:post_id>", views.like, name="like"),
    path("prof_posts", views.prof_posts, name="prof_posts"),
    path("post/<int:post_id>", views.post, name="post"),
    path("posts/<str:profile>", views.posts, name="posts"),
    path("follow/<int:user_id>", views.follow, name="follow")
]
