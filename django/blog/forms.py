"""This module contains forms of our django app."""

from django import forms

from .models import Comment, Post


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
