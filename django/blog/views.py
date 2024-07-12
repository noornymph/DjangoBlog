"""This module contains the view of our django app."""

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CommentForm, PostForm
from .models import Post


def post_list(request):
    """This view represents the list of the posts."""
    posts = Post.objects.filter(published_date__lte=timezone.now()).order_by(
        "published_date"
    )
    return render(request, "blog/post_list.html", {"posts": posts})


def post_detail(request, pk):
    """This view represents the post details"""
    post = get_object_or_404(Post, pk=pk)
    return render(request, "blog/post_detail.html", {"post": post})


@login_required
def post_new(request):
    """This view represents the creation of the  post."""
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm()
    return render(request, "blog/post_edit.html", {"form": form})


@login_required
def post_edit(request, pk):
    """This view represents the editing of the post."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_edit.html", {"form": form})


@login_required
def post_draft_list(request):
    """This view represents the draft of the post."""
    posts = Post.objects.filter(published_date__isnull=True).order_by("created_date")
    return render(request, "blog/post_draft_list.html", {"posts": posts})


def post_publish(request, pk):
    """This view represents the publishing of the post."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.publish()
    return redirect("post_detail", pk=pk)


@login_required
def post_remove(request, pk):
    """This view represents the deletion of the post."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
    return redirect("post_list")


def add_comment_to_post(request, pk):
    """This view represents the addition of comments to the post."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect("post_detail", pk=post.pk)
    else:
        form = CommentForm()
    return render(request, "blog/add_comment_to_post.html", {"form": form})


def logout_view(request):
    """This view deals with logging out"""
    logout(request)
    return redirect("post_list")
