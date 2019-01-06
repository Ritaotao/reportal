from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.
class Group(models.Model):
    name = models.CharField(max_length=200, unique=True)
    create_date = models.DateTimeField(default=timezone.now)
    def __str__(self):
        return self.name


class Role(models.Model):
    name = models.CharField(max_length=200, unique=True)
    create_date = models.DateTimeField(default=timezone.now)
    can_create = models.BooleanField(default=False)
    can_update = models.BooleanField(default=False)
    can_delete = models.BooleanField(default=False)
    can_submit = models.BooleanField(default=True)
    def __str__(self):
        return self.name


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profiles')
    role = models.ForeignKey(Role, default=1, on_delete=models.SET_DEFAULT)
    group = models.ForeignKey(Group, default=1, on_delete=models.SET_DEFAULT)
    title = models.CharField(max_length=200, default='', blank=True)
    organization = models.CharField(max_length=200, default='', blank=True)

"""
def create_profile(sender, **kwargs):
    user = kwargs["instance"]
    if kwargs["created"]:
        profile = Profile(user=user)
        profile.save()
post_save.connect(create_profile, sender=User)"""