from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin,
)
from optionsets_management.models import UserTypes


class UserAccountManager(BaseUserManager):
    def create_user(self, email, password=None, **kwargs):
        print("Create user called")
        if not email:
            raise ValueError("Users must have an email address")

        email = self.normalize_email(email)
        email = email.lower()

        # Check if the user already exists with the provided email
        existing_user = self.model.objects.filter(email=email).first()
        if existing_user:
            return existing_user

        user = self.model(email=email, **kwargs)

        user.set_password(password)
        user.user_type = UserTypes.objects.filter(name="Employer").first()
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **kwargs):
        user = self.create_user(email, password=password, **kwargs)

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class UserAccount(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=255, null=True, default="")
    first_name = models.CharField(max_length=255, null=True, default="", blank=True)
    last_name = models.CharField(max_length=255, null=True, default="", blank=True)
    email = models.EmailField(unique=True, max_length=255)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now=True)
    role = models.CharField(max_length=255, default="user")

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    user_type = models.ForeignKey(
        UserTypes,
        on_delete=models.CASCADE,
        related_name="user_type",
        null=True,
        default=None,
        blank=True,
    )

    mobile_number = models.CharField(max_length=255, null=True, blank=True)
    date_of_birth = models.DateField(max_length=255, null=True, blank=True)
    image = models.ImageField(upload_to="profile_images/", null=True, blank=True)

    objects = UserAccountManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return self.email

    def __str__(self):
        return self.email
