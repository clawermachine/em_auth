from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes

from .models import User, Role, Permission, AccessRule
from .serializers import RegisterSerializer, UserSerializer

def is_admin(user):
    # упрощённая проверка — если email admin@example.com
    # (позже можно через AccessRule)
    return user.email == "admin@example.com"


# регистрация
class RegisterView(generics.CreateAPIView):
    permission_classes = [AllowAny]
    queryset = User.objects.all()
    serializer_class = RegisterSerializer


# личный профиль
class ProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

    def put(self, request):
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def delete(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({"detail": "Account deleted"}, status=200)

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_roles(request):
    if not is_admin(request.user):
        return Response({"detail": "Forbidden"}, status=403)

    roles = Role.objects.all().values("id", "name")
    return Response(list(roles))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_permissions(request):
    if not is_admin(request.user):
        return Response({"detail": "Forbidden"}, status=403)

    permissions = Permission.objects.all().values("id", "name")
    return Response(list(permissions))


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_accessrules(request):
    if not is_admin(request.user):
        return Response({"detail": "Forbidden"}, status=403)

    accessrules = AccessRule.objects.all().values("id", "resource", "role_id", "permission_id")
    return Response(list(accessrules))


@api_view(["POST", "DELETE"])
@permission_classes([IsAuthenticated])
def manage_role_permissions(request, role_id):
    if not is_admin(request.user):
        return Response({"detail": "Forbidden"}, status=403)

    perm_id = request.data.get("permission_id")
    resource = request.data.get("resource")

    if not perm_id or not resource:
        return Response({"detail": "permission_id and resource are required"}, status=400)

    try:
        role = Role.objects.get(id=role_id)
        perm = Permission.objects.get(id=perm_id)
    except (Role.DoesNotExist, Permission.DoesNotExist):
        return Response({"detail": "Role or Permission not found"}, status=404)

    if request.method == "POST":
        # добавить
        from django.db import IntegrityError
        try:
            AccessRule.objects.create(role=role, permission=perm, resource=resource)
            return Response({"detail": "Permission added"}, status=201)
        except IntegrityError:
            return Response({"detail": "Permission already exists"}, status=400)

    if request.method == "DELETE":
        deleted, _ = AccessRule.objects.filter(
            role=role, permission=perm, resource=resource
        ).delete()
        if deleted:
            return Response({"detail": "Permission removed"}, status=200)
        return Response({"detail": "Permission not found"}, status=404)
