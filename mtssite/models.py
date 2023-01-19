from email.policy import default
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)

# Create your models here.
class Office(models.Model):
    officename = models.CharField(max_length=255, unique=True)
    officeaddress = models.CharField(max_length=255)
    officeheadinfo = models.ForeignKey('CustomUser', on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.officename

    def get_office_info(self):
        info = {
            'Номер офиса': self.officename,
            'Адрес офиса': self.officeaddress,
            'Руководитель': self.officeheadinfo.get_full_name(),
            'Табельный номер': self.officeheadinfo.get_personnel_number(),
        }
        return info

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


class ProdCodes(models.Model):
    code = models.CharField(max_length=20, unique=True)
    type = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return f"Code: {self.code}, Type: {self.type}"


class Product(models.Model):
    prod_name = models.CharField(max_length=255, unique=True)
    code = models.ForeignKey(ProdCodes, on_delete=models.PROTECT)
    manufacturer = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.prod_name

    def get_prod_name(self):
        return self.prod_name

    def get_code(self):
        return self.code

    def get_manufacturer(self):
        return self.manufacturer

    def get_description(self):
        return self.description


class ProductsInOffice(models.Model):
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    office_id = models.ForeignKey(Office, on_delete=models.PROTECT, to_field='officename')
    quantity = models.IntegerField(default=0)

    def get_product(self):
        return self.product

    def get_quantity(self):
        return self.quantity


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
            password=password,
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


class CustomUser(AbstractBaseUser, PermissionsMixin):
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

    def get_email(self):
        return self.email

    def get_personnel_number(self):
        return self.personnel_number

    def get_office_number(self):
        return self.shop_number

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_user_info(self):
        user_info = {
            'ФИО': self.fio,
            'Табельный номер': self.personnel_number,
            'Email': self.email,
            'Номер офиса': self.shop_number,
        }
        return user_info

    @property
    def is_staff(self):
        return self.is_admin

    def get_absolute_url(self):
        return reverse("user-profile-detail", kwargs={"pk": self.pk})