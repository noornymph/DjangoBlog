"""This module represents the model of the blog post"""

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


def get_today():
    """Returns the current date with timezone information."""
    return timezone.now().date()


class Post(models.Model):
    """This class represents the post model of our blog"""

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    likes = models.ManyToManyField(User, related_name="blogpost_like")

    objects = models.Manager()

    class Meta:
        """Meta options for the Post model."""

        permissions = [
            ("can_edit_post", "Can edit post"),
            ("can_delete_post", "Can delete post"),
            ("can_add_post", "Can add post"),
        ]

    # pylint: disable=no-member
    def number_of_likes(self):
        """This function counts the number of likes on the blog post"""
        return self.likes.count()

    def publish(self):
        """This function manages the publishing time and date"""
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return str(self.title)


class Comment(models.Model):
    """This class represents the comment model of our blog."""

    post = models.ForeignKey(
        "blog.Post", on_delete=models.CASCADE, related_name="comments"
    )
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        """This function contains the approval functionality."""
        self.approved_comment = True
        self.save()

    def __str__(self):
        return str(self.text)


class Profile(models.Model):
    "This function contains the profile model of the user."

    USER_CATEGORIES = [
        ("author", "Author"),
        ("editor", "Editor"),
        ("subscriber", "Subscriber"),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(blank=True)
    category = models.CharField(
        max_length=50, choices=USER_CATEGORIES, default="subscriber"
    )

    # pylint: disable=no-member
    def __str__(self):
        return str(self.user.username)
