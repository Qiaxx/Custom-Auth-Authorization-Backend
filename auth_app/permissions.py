from functools import wraps
from rest_framework.response import Response
from rest_framework import status
from auth_app.models import RolePermission, Permission


def has_permission(resource, action):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = getattr(request, 'user', None)
            if not user:
                return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

            permissions = Permission.objects.filter(
                rolepermission__role__userrole__user=user,
                resource=resource,
                action=action
            ).distinct()

            if not permissions.exists():
                return Response({'detail': 'Forbidden'}, status=status.HTTP_403_FORBIDDEN)

            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
