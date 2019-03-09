from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):

    def __str__(self):
        return self.email

    def has_settings(self):
        return hasattr(self, 'user_settings')