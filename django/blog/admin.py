"""This module represents the admin panel"""

from django.contrib import admin

from .models import Comment, Post, Profile


class ProfileAdmin(admin.ModelAdmin):
    """This class updates the admin interface to manage the category field."""

    list_display = ("user", "category")
    list_filter = ("category",)


admin.site.register(Profile, ProfileAdmin)
admin.site.register(Post)
admin.site.register(Comment)
