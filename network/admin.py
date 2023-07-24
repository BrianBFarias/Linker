from django.contrib import admin

from .models import Profile, User, Post

class ProfileAdmin(admin.ModelAdmin):
    filter_horizontal = ("followers", "following",)
    list_display = ('user', 'followers_count')

    def followers_count(self, obj):
        return len(obj.followers.all())


class PostAdmin(admin.ModelAdmin):
    list_display = ('creator', "content", "likes_count", "id")

    def likes_count(self, obj):
        return len(obj.likes.all())

admin.site.register(User)
admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post, PostAdmin)

# Register your models here.
