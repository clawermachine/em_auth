from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView
from .views import (RegisterView, ProfileView, list_roles, list_permissions, list_accessrules,
                    manage_role_permissions)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("profile/", ProfileView.as_view(), name="profile"),

    # кастомный JWT
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    # admin
    path("admin/roles/", list_roles, name="list_roles"),
    path("admin/permissions/", list_permissions, name="list_permissions"),
    path("admin/accessrules/", list_accessrules, name="list_accessrules"),
    path("admin/roles/<int:role_id>/permissions/", manage_role_permissions, name="manage_role_permissions"),
]
