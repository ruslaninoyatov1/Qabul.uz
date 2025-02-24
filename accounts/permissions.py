from rest_framework.permissions import BasePermission

class IsSuperAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "super_admin"

class IsBankOperator(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "bank_operator"

class IsGovernmentOfficer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "government_officer"

class IsBranchAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == "branch_admin"
