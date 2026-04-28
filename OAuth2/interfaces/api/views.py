from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from OAuth2.application.dto.login_dto import LoginDTO
from OAuth2.application.dto.register_dto import RegisterDTO
from OAuth2.application.dto.verify_mfa_dto import VerifyMFADTO
from OAuth2.domain.exceptions.auth_exceptions import (
    UserAlreadyExistsException,
    InvalidCredentialsException,
    InactiveUserException,
    UserNotFoundException,
    MFAChallengeNotFoundException,
    InvalidOrExpiredMFACodeException,
    MFAAttemptsExceededException,
)
from OAuth2.infrastructure.config.container import Container
from OAuth2.infrastructure.logging.logger import get_logger
from OAuth2.interfaces.api.serializers import (
    RegisterRequestSerializer,
    LoginRequestSerializer,
    VerifyMFARequestSerializer,
)


logger = get_logger(__name__)


class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto = RegisterDTO(**serializer.validated_data)

        try:
            use_case = Container.register_user_use_case()
            user = use_case.execute(dto)

            return Response({
                "message": "Usuario creado correctamente",
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "nombres": user.nombres,
                    "apellidos": user.apellidos,
                }
            }, status=status.HTTP_201_CREATED)

        except UserAlreadyExistsException as exc:
            logger.warning("Intento de registro con correo existente", extra={
                "event": "register_user_exists",
                "email": dto.email,
            })
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        except Exception:
            logger.exception("Error inesperado en registro")
            return Response({"detail": "Error interno del servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoginView(APIView):
    def post(self, request):
        serializer = LoginRequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto = LoginDTO(**serializer.validated_data)

        try:
            use_case = Container.login_user_use_case()
            result = use_case.execute(dto)

            return Response({
                "message": result.message,
                "mfa_required": result.mfa_required,
                "email": result.email,
                "access_token": result.access_token,
                "refresh_token": result.refresh_token,
                "user": None if result.user is None else {
                    "id": result.user.id,
                    "email": result.user.email,
                    "nombres": result.user.nombres,
                    "apellidos": result.user.apellidos,
                    "roles": result.user.roles,
                }
            }, status=status.HTTP_200_OK)

        except InvalidCredentialsException as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_401_UNAUTHORIZED)

        except InactiveUserException as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_403_FORBIDDEN)

        except Exception:
            logger.exception("Error inesperado en login")
            return Response({"detail": "Error interno del servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyMFAView(APIView):
    def post(self, request):
        serializer = VerifyMFARequestSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        dto = VerifyMFADTO(**serializer.validated_data)

        try:
            use_case = Container.verify_mfa_use_case()
            result = use_case.execute(dto)

            return Response({
                "message": result.message,
                "mfa_required": result.mfa_required,
                "access_token": result.access_token,
                "refresh_token": result.refresh_token,
                "user": None if result.user is None else {
                    "id": result.user.id,
                    "email": result.user.email,
                    "nombres": result.user.nombres,
                    "apellidos": result.user.apellidos,
                    "roles": result.user.roles,
                }
            }, status=status.HTTP_200_OK)

        except UserNotFoundException as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        except MFAChallengeNotFoundException as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        except InvalidOrExpiredMFACodeException as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_400_BAD_REQUEST)

        except MFAAttemptsExceededException as exc:
            return Response({"detail": str(exc)}, status=status.HTTP_429_TOO_MANY_REQUESTS)

        except Exception:
            logger.exception(
                "Error inesperado en login",
                event="login_unexpected_error",
            )
            return Response({"detail": "Error interno del servidor"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)