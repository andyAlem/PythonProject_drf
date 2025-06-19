from rest_framework import permissions


class IsModer(permissions.BasePermission):
    """класс для проверки является ли пользователь модератором"""

    message = "Вы не являетесь модератором"

    def has_permission(self, request, view):
        return request.user.groups.filter(name="moders").exists()


class IsOwner(permissions.BasePermission):
    """
    Проверка является ли пользователь владельцем объекта
    """

    def has_object_permission(self, request, view, obj):
        return obj == request.user
