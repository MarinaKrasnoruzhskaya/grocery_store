from rest_framework import permissions

from cart.models import Cart, CartProduct


class IsOwner(permissions.BasePermission):
    """
    Разрешение на уровне объекта, позволяющее авторизированным пользователям осуществлять операции по
    эндпоинтам со своей корзиной
    """

    def has_object_permission(self, request, view, obj):
        if (isinstance(obj, Cart) and obj.user == request.user or
                isinstance(obj, CartProduct) and obj.cart.user == request.user):
            return True
        return False
