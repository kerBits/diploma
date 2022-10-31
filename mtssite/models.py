from email.policy import default
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager
)

# Create your models here.
class Office(models.Model):
    officename = models.CharField(max_length=255, unique=True)
    officeaddress = models.CharField(max_length=255)
    officehead = models.CharField(max_length=255)
    officeheadtnumber = models.CharField(max_length=255)

    def get_absolute_url(self):
        return reverse("office-detail", kwargs={"pk": self.pk})
    
    
class News(models.Model):
    title = models.CharField(max_length=255)
    subtitle = models.CharField(max_length=255, blank=True)
    slug = models.SlugField(max_length=255, unique=True)
    body = models.TextField()
    meta_description = models.CharField(max_length=150, blank=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(blank=True, null=True)
    published = models.BooleanField(default=False)

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='personnel_number')


class CustomUserManager(BaseUserManager):
    def create_user(self, personnel_number, email, fio, password, shop_number=None):
        if not personnel_number:
            raise ValueError("Enter personnel number")

        if not email:
            raise ValueError("Enter email address")

        if not fio:
            raise ValueError("Enter FIO")

        user = self.model(
            personnel_number=personnel_number,
            email=self.normalize_email(email),
            fio=fio,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, personnel_number, email, fio, password, shop_number=None):
        user = self.create_user(
            personnel_number=personnel_number,
            email=email,
            fio=fio,
            password=password,
            shop_number=shop_number,
        )

        user.is_admin = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    personnel_number = models.CharField(max_length=20, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    fio = models.CharField(max_length=255)
    shop_number = models.ForeignKey(Office, on_delete=models.CASCADE, to_field='officename', null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'personnel_number'
    REQUIRED_FIELDS = ['email', 'fio',]

    def get_full_name(self):
        return self.fio

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin