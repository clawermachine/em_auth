from rest_framework import serializers
from .models import User, Role


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ("id", "first_name", "last_name", "middle_name", "email", "password", "password_2")

    def validate(self, attrs):
        if attrs["password"] != attrs["password_2"]:
            raise serializers.ValidationError({"password": "Passwords don't match"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password_2")
        user_role = Role.objects.get(name="user")

        user = User(
            first_name=validated_data["first_name"],
            last_name=validated_data.get("last_name"),
            middle_name=validated_data.get("middle_name"),
            email=validated_data["email"],
            role=user_role
        )
        user.set_password(validated_data["password"])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ("password",)
