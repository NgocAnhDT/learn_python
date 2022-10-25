from datetime import datetime

from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class ModelManager(models.Manager):
    def get_queryset(self):
        return super(ModelManager, self).get_queryset().filter(deleted_at__isnull=True)


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True, verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='updated at')
    deleted_at = models.DateTimeField(
        default=None, blank=True, null=True, verbose_name='deleted at')

    objects = ModelManager()

    class Meta:
        abstract = True

    def delete(self, *args, **kwargs):
        self.deleted_at = datetime.now()
        self.save()


class User(AbstractUser, BaseModel):
    address = models.TextField()
    phone = models.CharField(max_length=11)
    avatar = models.ImageField(upload_to='images/', null=True)

    objects = UserManager()


class Product(BaseModel):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.FloatField()

    def __str__(self):
        return self.name


class Insurance(BaseModel):
    warranty_period = models.IntegerField()
    date_of_purchase = models.DateField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    STATUS_CHOICES = [
        ('ac', 'active'),
        ('ex', 'expired'),
    ]
    status = models.CharField(max_length=2, choices=STATUS_CHOICES, default='ac')
