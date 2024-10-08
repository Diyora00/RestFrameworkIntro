from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def generate_token(sender, instance, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
