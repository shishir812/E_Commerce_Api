from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('employee', 'Employee'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='customer')

    groups = models.ManyToManyField(
        Group,
        related_name="user_app_user_set",
        blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="user_app_user_set",
        blank=True
    )

    def save(self, *args, **kwargs):
        if self.role != 'customer' and not self.is_superuser:
            raise ValueError("Only superusers can assign roles other than customer.")
        super().save(*args, **kwargs)
