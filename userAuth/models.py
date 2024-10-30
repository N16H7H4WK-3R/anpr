from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    SUPERUSER = 'superuser'
    SUB_ADMIN = 'sub_admin'
    MEMBER = 'member'

    ROLE_CHOICES = [
        (SUPERUSER, 'SuperUser'),
        (SUB_ADMIN, 'Sub Admin'),
        (MEMBER, 'Member User'),
    ]

    role = models.CharField(
        max_length=50, choices=ROLE_CHOICES, default=MEMBER)

    def is_sub_admin(self):
        return self.role == self.SUB_ADMIN

    def is_member(self):
        return self.role == self.MEMBER

    def __str__(self):
        return self.username
