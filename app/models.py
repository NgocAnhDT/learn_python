from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django_softdelete.models import SoftDeleteModel, DeletedManager

class User(AbstractUser, SoftDeleteModel):
    address = models.TextField()
    phone = models.CharField(max_length=11)

    objects = UserManager()
    deleted_objects = DeletedManager()
