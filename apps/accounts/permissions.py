from rest_framework.permissions import BasePermission

class IsSelfOrAdmin(BasePermission):
    """اجازه ویرایش فقط به خود کاربر یا ادمین"""
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj == request.user
