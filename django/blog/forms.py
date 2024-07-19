"""This module contains forms of our django app."""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import Comment, Post, Profile


class PostForm(forms.ModelForm):
    """This class represents the post form."""

    class Meta:
        """This class represents the structure of the post."""

        model = Post
        fields = (
            "title",
            "text",
        )


class CommentForm(forms.ModelForm):
    """This class represnts the comment form."""

    class Meta:
        """This class represents the structure of the post."""

        model = Comment
        fields = (
            "author",
            "text",
        )


class SignUpForm(UserCreationForm):
    """This class represents the sign-up form."""

    email = forms.EmailField(required=True)

    class Meta:
        """This class represents the structure of sign-up form"""

        model = User
        fields = ("username", "email", "password1", "password2")


class ProfileForm(forms.ModelForm):
    """This class represents the profile form."""

    class Meta:
        """This class represents the structure of  profile form."""

        model = Profile
        fields = ("bio", "category")
