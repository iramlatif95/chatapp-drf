
from rest_framework import permissions

class IsGroupOwnerOrReadOnly(permissions.BasePermission):
   

    def has_object_permission(self, request, view, obj):
        
        if request.method in permissions.SAFE_METHODS:
            return True
        
       
        if request.method == 'DELETE':
            return obj.created_by == request.user

        return True
