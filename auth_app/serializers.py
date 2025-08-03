import hashlib

from rest_framework import serializers

from auth_app.models import Role, Permission, UserRole, RolePermission, User



class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    password_repeat = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = (
            "email",
            "first_name",
            "last_name",
            "patronymic",
            "password",
            "password_repeat",
        )

    def validate(self, data):
        if data["password"] != data["password_repeat"]:
            raise serializers.ValidationError("Passwords do not match.")
        return data

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password_repeat")
        password_hash = hashlib.sha256(password.encode()).hexdigest()
        user = User.objects.create(password_hash=password_hash, **validated_data)
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "email", "first_name", "last_name", "patronymic")

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'


class PermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Permission
        fields = '__all__'


class UserRoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserRole
        fields = '__all__'


class RolePermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolePermission
        fields = '__all__'
