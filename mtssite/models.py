from email.policy import default
from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.urls import reverse

# Create your models here.
class Office(models.Model):
    officename = models.CharField(max_length=255)
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

    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='username')