from rest_framework.permissions import BasePermission

class HasRole(BasePermission):
    def __init__(self, role_name):
        self.role_name = role_name

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated 
            and request.user.role 
            and request.user.role.name == self.role_name
        )

class IsAdmin(HasRole):
    def __init__(self):
        super().__init__("admin")

class IsStudent(HasRole):
    def __init__(self):
        super().__init__("student")

class IsTeacher(HasRole):
    def __init__(self):
        super().__init__("teacher")

class IsSales(HasRole):
    def __init__(self):
        super().__init__("sales")
