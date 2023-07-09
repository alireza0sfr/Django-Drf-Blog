from django.contrib.auth.models import BaseUserManager
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):

    def create_user(self, email, password, **kwargs):

        if self.args_validator(email, password, **kwargs):
            email = self.normalize_email(email)
            user = self.model(email=email, **kwargs)
            user.set_password(password)
            user.save()
            return user

    def create_superuser(self, email, password, **kwargs):

        if self.model.objects.filter(is_superuser=True).count() >= 1:
            raise ValueError(_('Superuser is Already Created!'))

        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('is_staff', True)
        kwargs.setdefault('is_active', True)
        kwargs.setdefault('is_anonymous', True)
        kwargs.setdefault('is_verified', True)

        if not kwargs.get('is_superuser'):
            raise ValueError(_('Superuser must have is_superuser=True'))

        if not kwargs.get('is_anonymous'):
            raise ValueError(_('Superuser must have is_anonymous=True'))

        if not kwargs.get('is_active'):
            raise ValueError(_('Superuser must have is_active=True'))

        if not kwargs.get('is_staff'):
            raise ValueError(_('Superuser must have is_staff=True'))

        if not kwargs.get('is_verified'):
            raise ValueError(_('Superuser must have is_verified=True'))

        return self.create_user(email, password, **kwargs)

    @staticmethod
    def args_validator(email, password, **kwargs):
        if not email:
            raise ValueError(_('Email Must Be Set!'))

        if not password:
            raise ValueError(_('Set Password!'))

        return True
