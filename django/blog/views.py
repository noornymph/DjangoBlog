"""This module contains the views of our Django app."""

from blog.models import Post, Profile
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required, permission_required
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import CommentForm, PostForm, ProfileForm, SignUpForm


def signup(request):
    """The view represents the sign-up form"""

    if request.method == "POST":
        form = SignUpForm(request.POST)
        profile_form = ProfileForm(request.POST)
        if form.is_valid() and profile_form.is_valid():
            user = form.save()
            profile = Profile(user=user, **profile_form.cleaned_data)
            profile.save()
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect("post_list")
    else:
        form = SignUpForm()
        profile_form = ProfileForm()
    return render(
        request,
        "registration/signup.html",
        {"form": form, "profile_form": profile_form},
    )


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
@permission_required("blog.can_add_post", raise_exception=True)
def post_new(request):
    """This view represents the creation of a new post."""
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_detail", pk=post.pk)
        else:
            return render(request, "blog/post_edit.html", {"form": form})
    else:
        form = PostForm()
    return render(request, "blog/post_edit.html", {"form": form})


@login_required
@permission_required("blog.can_edit_post", raise_exception=True)
def post_edit(request, pk):
    """This view represents the editing of an existing post."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect("post_detail", pk=post.pk)
        else:
            return render(request, "blog/post_edit.html", {"form": form})
    else:
        form = PostForm(instance=post)
    return render(request, "blog/post_edit.html", {"form": form})


@login_required
@permission_required("blog.can_delete_post", raise_exception=True)
def post_remove(request, pk):
    """This view represents the deletion of a post."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.delete()
        return redirect("post_list")
    return redirect("post_list")


@login_required
def post_draft_list(request):
    """This view represents the drafts of posts."""
    posts = Post.objects.filter(published_date__isnull=True).order_by("created_date")
    return render(request, "blog/post_draft_list.html", {"posts": posts})


@login_required
def post_publish(request, pk):
    """This view represents the publishing of a post."""
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        post.publish()
    return redirect("post_detail", pk=post.pk)


@login_required
def blog_post_like(request, pk):
    """This view is related to the number of likes on the blog post."""
    post = get_object_or_404(Post, pk=pk)
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)
    return redirect("post_detail", pk=post.pk)


@login_required
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


def categorized_users(request):
    """View to display users categorized by their roles"""
    authors = Profile.objects.filter(category="author")
    editors = Profile.objects.filter(category="editor")
    subscribers = Profile.objects.filter(category="subscriber")

    context = {
        "authors": authors,
        "editors": editors,
        "subscribers": subscribers,
    }
    return render(request, "blog/categorized_users.html", context)


def permission_denied(request, exception):
    """View to render the permission denied page."""
    return render(
        request,
        "blog/permission_denied.html",
        {"message": "You do not have the rights to perform this operation!!"},
    )
