from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from phonenumber_field.modelfields import PhoneNumberField
from .managers import UserManager

class User(AbstractBaseUser):
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)
    email = models.EmailField(max_length=100)
    full_name = models.CharField(max_length=100)    
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_verify = models.BooleanField(default=False)
    likes = models.ManyToManyField('shop.Product', blank=True, related_name='likes')
    # set a manager role for shop manager to access orders and products
    is_manager = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_created=True,auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD ='phone_number'


    def __str__(self):
        return f"{self.phone_number}"

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin
"""
    def get_likes_count(self):
        return self.likes.count()
"""

