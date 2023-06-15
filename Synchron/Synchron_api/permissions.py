from rest_framework.permissions import BasePermission

class IsScrumMasterOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'GET':
            return True
        if not request.user.is_authenticated:
            return False
        return request.user.profile.position == 'SM'
