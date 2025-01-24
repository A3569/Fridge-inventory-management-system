from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User

class NoPasswordBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            return None 