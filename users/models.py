from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    #def create_superuser(self, email, password=None, **extra_fields):
    #    extra_fields.setdefault("is_staff", True)
    #    extra_fields.setdefault("is_superuser", True)
    #    return self.create_user(email, password, **extra_fields)


class Role(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50, blank=True, null=True)
    middle_name = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    #is_superuser = models.BooleanField(default=False)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, null=False, blank=False, default=None)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email

class Permission(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class AccessRule(models.Model):
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    permission = models.ForeignKey(Permission, on_delete=models.CASCADE)
    resource = models.CharField(max_length=100)
    allowed = models.BooleanField(default=True)

    class Meta:
        unique_together = ('role', 'permission', 'resource')

    def __str__(self):
        return f"{self.role} -> {self.permission} @ {self.resource}"
