from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE
from django.db.models.fields.related import OneToOneField

class UserProfile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    viewTour = models.BooleanField(default=True)

    def delete(self, *args, **kwargs):
        self.user.delete()
        return super(self.__class__, self).delete(*args, **kwargs)