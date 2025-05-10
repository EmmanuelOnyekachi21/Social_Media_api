from django.db import models

# Create your models here.
import uuid
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import get_object_or_404


class UserManager(BaseUserManager):
    def get_object_by_public_id(self, public_id):
        return get_object_or_404(self.model, public_id=public_id)
    
    def create_user(self, username, email, password=None, **kwargs):
        """
        Create and return a `User` with an \
            email, phone number, username and password.
        """
        if username is None:
            raise TypeError("User must have a username")
        
        if email is None:
            raise TypeError('Users must have an email')
        
        if password is None:
            raise TypeError('User must have password.')
        
        user = self.model(
            username=username, email=self.normalize_email(email), **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)

        return user
    
    def create_superuser(self, username, email, password=None, **kwargs):
        """
        Create and return a user with admin privileges
        """
        if password is None:
            raise TypeError('Superusers must have passwords')
        
        if email is None:
            raise TypeError('Superusers must have an email')
        
        if username is None:
            raise TypeError("Superuser must have a username")
        
        user = self.create_user(username, email, password, **kwargs)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    public_id = models.UUIDField(
        db_index=True, unique=True, default=uuid.uuid4, editable=False
    )
    username = models.CharField(db_index=True, max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(
        db_index=True,
        unique=True
    )
    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True)
    
    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = UserManager()

    def __str__(self):
        return f'{self.email}'
    
    @property
    def name(self):
        return f'{self.first_name} {self.last_name}'