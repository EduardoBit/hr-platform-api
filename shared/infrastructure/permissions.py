from rest_framework.permissions import BasePermission
from shared.constants import RolesUsuario


class IsSuperAdmin(BasePermission):
    message = "No tienes permisos para realizar esta acción."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "rol", None) == RolesUsuario.SUPERADMIN
        )


class IsPropietario(BasePermission):
    message = "No tienes permisos para realizar esta acción."

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and getattr(request.user, "rol", None) == RolesUsuario.PROPIETARIO
        )


class IsSuperAdminOrPropietario(BasePermission):
    message = "No tienes permisos para realizar esta acción."

    def has_permission(self, request, view):
        rol = getattr(request.user, "rol", None)
        return (
            request.user
            and request.user.is_authenticated
            and rol in {RolesUsuario.SUPERADMIN, RolesUsuario.PROPIETARIO}
        )