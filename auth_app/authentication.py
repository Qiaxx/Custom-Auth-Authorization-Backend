from functools import wraps

from rest_framework import status
from rest_framework.response import Response

from auth_app.models import User
from auth_app.tokens import verify_token


def authenticate(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth_header = request.headers.get("Authorization")
        if not auth_header or not auth_header.startswith("Bearer "):
            return Response(
                {"detail": "Authorization header missing or invalid"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        token = auth_header.split(" ")[1]
        user_id = verify_token(token)

        if not user_id:
            return Response(
                {"detail": "Invalid or expired token"},
                status=status.HTTP_401_UNAUTHORIZED,
            )

        try:
            user = User.objects.get(id=user_id, is_active=True)
        except User.DoesNotExist:
            return Response(
                {"detail": "User not found"}, status=status.HTTP_401_UNAUTHORIZED
            )

        request.user = user
        return view_func(request, *args, **kwargs)

    return _wrapped_view
