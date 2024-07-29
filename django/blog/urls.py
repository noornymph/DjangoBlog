"""This module contains the URLs of our Django app."""

from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

urlpatterns = [
    path("", views.post_list, name="post_list"),
    path("post/<int:pk>/", views.post_detail, name="post_detail"),
    path("post/new/", views.post_new, name="post_new"),
    path("post/<int:pk>/edit/", views.post_edit, name="post_edit"),
    path("drafts/", views.post_draft_list, name="post_draft_list"),
    path("post/<int:pk>/publish/", views.post_publish, name="post_publish"),
    path("post/<int:pk>/remove/", views.post_remove, name="post_remove"),
    path(
        "post/<int:pk>/comment/", views.add_comment_to_post, name="add_comment_to_post"
    ),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path(
        "accounts/logout/",
        auth_views.LogoutView.as_view(template_name="registration/logout.html"),
        name="logout",
    ),
    path("post/<int:pk>/like/", views.blog_post_like, name="blog_post_like"),
    path("signup/", views.signup, name="signup"),
    path("categorized_users/", views.categorized_users, name="categorized_users"),
    path("permission-denied/", views.permission_denied, name="permission_denied"),
]

handler403 = "blog.views.permission_denied"
