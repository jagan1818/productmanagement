from unittest.mock import Base
from rest_framework.permissions import BasePermission
from products.models import *

class AdminPermission(BasePermission):
    def has_permission(self, request, view):
        us = User.objects.get(username=request.user)  
        u = UserProfile.objects.get(user_id=us.id)
        if u.role_id == 1:
            return True
        return False

class ManagerPermission(BasePermission):
    def has_permission(self, request, view):
        us = User.objects.get(username=request.user)
        u = UserProfile.objects.get(user_id=us.id)
        if u.role_id == 2:
            return True
        return False

class AdminOrManagerPermission(BasePermission):
    def has_permission(self, request, view):
        us = User.objects.get(username=request.user)
        u = UserProfile.objects.get(user_id=us.id)
        if u.role_id == 1 or u.role_id == 2:
            return True
        return False
