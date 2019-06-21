from __future__ import unicode_literals
from django.db import models
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Createa an errors class to keep track of validation
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name should be at least 2 characters'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name should be at least 2 characters'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Email must be of valid format'
        if len(postData['password']) < 8:
            errors['password'] = 'Password should be at least 8 characters'
        return errors
        
# Create your models here.
class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()
