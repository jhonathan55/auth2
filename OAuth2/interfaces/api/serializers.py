from rest_framework import serializers


class RegisterRequestSerializer(serializers.Serializer):
    nombres = serializers.CharField(max_length=80)
    apellidos = serializers.CharField(max_length=80)
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)


class LoginRequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)


class VerifyMFARequestSerializer(serializers.Serializer):
    email = serializers.EmailField()
    code = serializers.CharField(min_length=6, max_length=6)