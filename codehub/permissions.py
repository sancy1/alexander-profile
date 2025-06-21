
# codehub/permissions.py

from rest_framework import permissions

class IsOwnerOfUserHistory(permissions.BasePermission):
    """
    Custom permission to only allow owners of a UserHistory object to view or edit it.
    """
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD, or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the UserHistory.
        return obj.user == request.user