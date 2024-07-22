import sys

from django.contrib.auth.models import Permission
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Profile


@receiver(post_save, sender=Profile)
def assign_permissions(sender, instance, created, **kwargs):
    """
    Assigns permissions to the user based on their profile category.

    Args:
        sender (Model): The model class that triggered the signal.
        instance (Profile): The instance of the Profile model.
        created (bool): Boolean indicating if a new instance was created.
        kwargs (dict): Additional keyword arguments.
    """
    if created or instance.category in ["author", "editor"]:
        # Clear existing permissions
        instance.user.user_permissions.clear()

        if instance.category == "author":
            permissions = ["can_add_post", "can_edit_post", "can_delete_post"]
        elif instance.category == "editor":
            permissions = ["can_edit_post"]
        else:
            permissions = []

        for perm in permissions:
            try:
                permission = Permission.objects.get(codename=perm)
                instance.user.user_permissions.add(permission)
            except Permission.DoesNotExist:
                # Print a message if the permission does not exist
                print(f"Permission '{perm}' does not exist.", file=sys.stderr)
