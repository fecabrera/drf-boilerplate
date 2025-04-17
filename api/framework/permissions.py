from rest_framework.permissions import *  # noqa


class IsNotAuthenticated(BasePermission):
    """
    Allows access only to unauthenticated users.
    """

    def has_permission(self, request, view):
        return not bool(request.user and request.user.is_authenticated)


class IsNotAuthenticatedOrReadOnly(BasePermission):
    """
    The request is unauthenticated as a user, or is a read-only request.
    """

    def has_permission(self, request, view):
        if bool(
                request.user and
                request.user.is_authenticated
        ):
            return request.method in SAFE_METHODS
        else:
            return request.method not in SAFE_METHODS
