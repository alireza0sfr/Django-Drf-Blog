from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from phonenumber_field.modelfields import PhoneNumberField

from common.models import BaseModel
from managers.accounts import UserManager
from enums.accounts import BanReasons


class User(BaseModel, AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=255, unique=True)
    phone_number = PhoneNumberField(null=True, blank=True, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_anonymous = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email


class Profile(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    image = models.ImageField(blank=True, null=True)
    bio = models.TextField(max_length=600, blank=True, null=True)

    @property
    def full_name(self):
        return f'{self.first_name} {self.last_name}' if self.first_name else self.user.email

    def __str__(self):
        return self.full_name


class BaseBanModel(BaseModel):
    until = models.DateTimeField()
    reason = models.CharField(default=BanReasons.ABUSIVE, choices=BanReasons.choices, max_length=20)
    description = models.TextField(max_length=255, blank=True, null=True)


class UserBan(BaseBanModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.__str__()


class IPBan(BaseBanModel):
    ip = models.GenericIPAddressField(unique=True, unpack_ipv4=True)

    def __str__(self):
        return self.ip


@receiver(post_save, sender=User)
def save_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
