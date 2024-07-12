"""This module represents the admin panel"""

from django.contrib import admin

from .models import Comment, Post

admin.site.register(Post)
admin.site.register(Comment)
