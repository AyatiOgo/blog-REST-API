from django.db import models
from django.contrib.auth.models import AbstractUser
from django_api.settings import AUTH_USER_MODEL
from autoslug import AutoSlugField
from django.utils import timezone
# Create your models here.

class CustomUSer(AbstractUser):
    bio = models.TextField(blank=True, null=True)
    profile_img = models.ImageField(upload_to='profile_img', blank=True, null=True)
    facebook = models.URLField(max_length=255, blank=True, null=True)
    instagram = models.URLField(max_length=255, blank=True, null=True)
    twitter = models.URLField(max_length=255, blank=True, null=True)
    linkedin = models.URLField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.username
    

class Blog(models.Model):

    CATEGORY = (
        ('Business', 'Business'),
        ('Sports', 'Sports'),
        ('Lifestyle', 'Lifestyle'),
    )

    title = models.CharField(max_length=255)
    slug = AutoSlugField(populate_from='title', unique=True, blank=True, null=True, always_update=True)
    content = models.TextField()
    author = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.SET_NULL, related_name='blogs', null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    is_draft = models.BooleanField(default=True)
    category = models.CharField(max_length=255, choices=CATEGORY, blank=True, null=True)
    featured_img = models.ImageField(upload_to='blog-img', null=True, blank=True)


    class Meta:
        ordering = ['-published_time']

    def save(self,*args, **kwargs ):

        if not self.is_draft and self.published_time is None:
            self.published_time = timezone.now()

        super().save(*args, **kwargs)