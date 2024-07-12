"""This module contains the configuration details."""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    """This class represents the configurations of our blog."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "blog"
