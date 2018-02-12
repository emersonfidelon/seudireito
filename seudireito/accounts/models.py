import re

from django.db import models
from django.utils import timezone
from django.core.mail import send_mail
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings


class UserManager(BaseUserManager):

    def _create_user(self, username, email, password, is_staff, is_superuser, **extra_fields):
        now = timezone.now()
        
        email = self.normalize_email(email)
        user = self.model(
                 username=email,   
                 email=email,
                 is_staff=is_staff, is_active=True,
                 is_superuser=is_superuser, last_login=now,
                 date_joined=now, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        return self._create_user(username, email, password, False, False, **extra_fields)

    def create_superuser(self, username, email, password, **extra_fields):
        user=self._create_user(username, email, password, True, True, **extra_fields)
        user.is_active=True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):

    username = models.CharField(_('username'), max_length=255, unique=True)
    name = models.CharField(_('name'), max_length=100)
    email = models.EmailField(_('email address'), max_length=255, unique=True)
    is_company = models.BooleanField(_('company'), default=False)
    is_lawyer = models.BooleanField(_('lawyer'), default=False)
    
    is_staff = models.BooleanField(_('staff status'), default=False, help_text=_('Designates whether the user can log into this admin site.'))
    is_active = models.BooleanField(_('active'), default=True, help_text=_('Designates whether this user should be treated as active. Unselect this instead of deleting accounts.'))
    date_joined = models.DateTimeField(_('date joined'), default=timezone.now)
    is_trusty = models.BooleanField(_('trusty'), default=False, help_text=_('Designates whether this user has confirmed his account.'))

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    objects = UserManager()

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
    
    def get_lawyer_profile(self):
        lawyer_profile = None
        if hasattr(self, 'lawyerprofile'):
            lawyer_profile = self.lawyerprofile
        return lawyer_profile
    
    def get_company_profile(self):
        company_profile = None
        if hasattr(self, 'companyprofile'):
            company_profile = self.companyprofile
        return company_profile

    def __str__(self):
        return self.name or email

    def get_full_name(self):
        return self.name

    def get_short_name(self):
        return str(self).split(" ")[0]

    def email_user(self, subject, message, from_email=None):
        send_mail(subject, message, from_email, [self.email])

class LawyerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telephone = models.CharField(_('telephone'), max_length=30)
    cpf = models.CharField(_('cpf'), max_length=15, unique=True)

class CompanyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activity = models.CharField(_('activity'), max_length=100)
