from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models


class CustomModelUser(AbstractUser):
    phoneNumberRegex = RegexValidator(regex=r"^\+?1?\d{8,15}$")
    phoneNumber = models.CharField(validators=[phoneNumberRegex], max_length=16, unique=True)


def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.user.id}/{filename}'


class UserProfile(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100, null=True)
    last_name = models.CharField(max_length=100, null=True)
    discount_size = models.DecimalField(max_digits=5, decimal_places=5,
                                        null=True)
    birthday = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to=user_directory_path)
    bio = models.TextField()

    def user_directory_path(instance, filename):
        return f'user_{instance.UserProfile.id}/{filename}'

    def __str__(self):
        return self.user.username
