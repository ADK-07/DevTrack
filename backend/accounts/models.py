from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


"""Custom manager: needed because we log in with EMAIL instead of USERNAME.
 Django's default manager (UserManager) builds users around a "username"
 field, so its create_user / create_superuser would break once we set
 username = None. This manager replaces them with email-based versions."""
 
 
 
class UserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        # Email is our login identifier, so it must always be provided.
        if not email:
            raise ValueError("Email address is required.")

        # Lowercases the domain part (Bob@EXAMPLE.com -> Bob@example.com).
        email = self.normalize_email(email)

        user = self.model(email=email, **extra_fields)

        # Hashes the password. Never store raw passwords.
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password=None, **extra_fields):
        # Called by `python manage.py createsuperuser`.
        # Set the flags a superuser needs, plus our custom role.
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("role", "admin")

        # Safety checks in case someone passes False explicitly.
        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=150)
    role = models.CharField(
        max_length=20,
        choices=[
            ("admin", "Admin"),
            ("manager", "Manager"),
            ("developer", "Developer"),
        ],
        default="developer",
    )

    # Attach our custom manager. Without this line, Django keeps using the
    # default manager (which expects a username), and User.objects.create_user()
    # and createsuperuser would fail with a TypeError.
    objects = UserManager()

    # Field used to log in (replaces username).
    USERNAME_FIELD = "email"

    # Extra fields `createsuperuser` prompts for (email and password are
    # always asked, so don't list them here).
    REQUIRED_FIELDS = ["full_name"]

    def __str__(self):
        return self.email