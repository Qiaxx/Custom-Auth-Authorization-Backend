from django.contrib.auth.backends import BaseBackend
from auth_app.models import User

class EmailBackend(BaseBackend):
    def authenticate(self, request, email=None, password=None):
        try:
            user = User.objects.get(email=email, is_active=True)
        except User.DoesNotExist:
            return None

        if user.check_password(password):
            return user
        return None

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None
