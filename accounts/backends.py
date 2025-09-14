from django.contrib.auth.backends import ModelBackend
from accounts.models import CustomUser

class EmailBackend(ModelBackend):
    """
    Authenticate using email instead of username.
    """
    def authenticate(self, request, username=None, password=None, **kwargs):
        email = kwargs.get('email') or username
        if email is None or password is None:
            return None
        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            return None
        if user.check_password(password) and self.user_can_authenticate(user):
            return user
        return None
