from django.contrib.auth import user_logged_in, user_logged_out
from django.core.cache import cache
from django.core.mail import send_mail
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.http import request

from MainApp.settings import EMAIL_HOST_USER
from .models import CustomModelUser, UserProfile
from shop_app.models import Backpack, ShoppingList
from .views import my_signal


@receiver(post_save, sender=CustomModelUser)
def update_profile_signal(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
        instance.userprofile.save()


# @receiver(post_save, sender=UserProfile)
# def update_profile_signal(sender, instance, created, **kwargs):
#     if created:
#         Backpack.objects.create(bayer=instance)
#         instance.backpack.save()
#         ShoppingList.objects.create(user_bayer=instance)
#
#         instance.shoppinglist.save()


@receiver(my_signal)
def my_callback(sender, **kwargs):
    text_message = "Congratulations! You were registered and can continue registration with UserProfile Form!"
    email = str(sender.email)
    send_mail('djangoProjectCBS',
              text_message,
              EMAIL_HOST_USER, [email],
              fail_silently=True,
              )


# @receiver(user_logged_in)
# def on_user_login(sender, **kwargs):
#     user_ = kwargs.get('user')
#     print(user_, "LOGINNN")


@receiver(user_logged_out)
def on_user_logout(sender, **kwargs):
    user = kwargs.get('user')
    cache.set(str(user), 'Offline', None)
