from django.db import models
from django.conf import settings
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    past_address = models.CharField(max_length=256)
    present_address = models.CharField(max_length=256)
    phone_number = models.CharField(max_length=256)

    def get_absolute_url(self):
        return reverse('details')
