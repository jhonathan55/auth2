from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError as DjangoValidationError
from django.db import transaction
import logging
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import AppUser, MFAChallenge
from .serializers import (
    ChangePasswordWithRecoverySerializer,
    LoginSerializer,
    PasswordRecoveryRequestSerializer,
    RegisterSerializer,
    VerifyMFASerializer,
    VerifyPasswordRecoveryCodeSerializer,
)
from .services.mfa_service import create_mfa_challenge, verify_mfa_code
from .services.email_service import send_mfa_email, send_password_reset_email
from .services.password_recovery_service import (
    PasswordRecoveryError,
    create_password_reset_challenge,
    consume_password_reset_challenge,
    get_verified_password_reset_challenge,
    verify_password_reset_code,
)


logger = logging.getLogger("OAuth2")


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response({
            "message": "Usuario creado correctamente",
            "user": {
                "id": user.id,
                "email": user.email,
                "nombres": user.nombres,
                "apellidos": user.apellidos,
            }
        }, status=status.HTTP_201_CREATED)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data["user"]
        user.last_login_at = timezone.now()
        user.save(update_fields=["last_login_at"])

        if user.mfa_enabled:
            _, code = create_mfa_challenge(user, purpose="LOGIN")
            send_mfa_email(user, code)

            return Response({
                "message": "Código MFA enviado al correo",
                "mfa_required": True,
                "email": user.email,
            }, status=status.HTTP_200_OK)

        return Response({
            "message": "Login exitoso",
            "mfa_required": False,
            "user": {
                "id": user.id,
                "email": user.email,
                "nombres": user.nombres,
                "apellidos": user.apellidos,
            }
        }, status=status.HTTP_200_OK)


class VerifyMFAView(APIView):
    def post(self, request):
        serializer = VerifyMFASerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        code = serializer.validated_data["code"]

        try:
            user = AppUser.objects.get(email=email)
        except AppUser.DoesNotExist:
            return Response({"detail": "Solicitud inválida"}, status=status.HTTP_400_BAD_REQUEST)

        challenge = MFAChallenge.objects.filter(
            user=user,
            purpose="LOGIN",
            consumed_at__isnull=True,
        ).order_by("-created_at").first()

        if not challenge:
            return Response({"detail": "No existe desafío MFA activo"}, status=status.HTTP_400_BAD_REQUEST)

        valid = verify_mfa_code(challenge, code)

        if not valid:
            return Response({"detail": "Código inválido o expirado"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message": "MFA validado correctamente",
            "user": {
                "id": user.id,
                "email": user.email,
            }
        }, status=status.HTTP_200_OK)


class RequestPasswordRecoveryView(APIView):
    def post(self, request):
        serializer = PasswordRecoveryRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = AppUser.objects.filter(email=email, is_active=True).first()

        if user:
            _, code = create_password_reset_challenge(user)
            send_password_reset_email(user, code)
            logger.info(
                "Password recovery requested for active user",
                extra={"event": "password_recovery_request_email_sent", "email": email},
            )
        else:
            logger.info(
                "Password recovery requested for non-existing or inactive user",
                extra={"event": "password_recovery_request_user_not_found", "email": email},
            )

        return Response({
            "message": "Si el correo existe, se enviará un código de recuperación",
        }, status=status.HTTP_200_OK)


class VerifyPasswordRecoveryCodeView(APIView):
    def post(self, request):
        serializer = VerifyPasswordRecoveryCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            verify_password_reset_code(
                email=serializer.validated_data["email"],
                code=serializer.validated_data["code"],
            )
        except PasswordRecoveryError:
            return Response({"detail": "Código inválido o expirado"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({
            "message": "Código validado correctamente",
            "password_recovery_verified": True,
        }, status=status.HTTP_200_OK)


class ChangePasswordWithRecoveryView(APIView):
    def post(self, request):
        serializer = ChangePasswordWithRecoverySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        new_password = serializer.validated_data["new_password"]

        with transaction.atomic():
            try:
                user, challenge = get_verified_password_reset_challenge(
                    email=serializer.validated_data["email"],
                    lock=True,
                )
            except PasswordRecoveryError:
                return Response({"detail": "Debes validar un código vigente antes de cambiar la contraseña"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                validate_password(new_password, user=user)
            except DjangoValidationError as error:
                return Response({"new_password": list(error.messages)}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(new_password)
            user.save(update_fields=["password", "updated_at"])
            consume_password_reset_challenge(challenge)

        return Response({
            "message": "Contraseña actualizada correctamente",
        }, status=status.HTTP_200_OK)
