# OAuth2/application/use_cases/login_user.py
from dataclasses import dataclass
from OAuth2.application.dto.auth_response_dto import AuthResponseDTO, AuthUserDTO
from OAuth2.application.dto.login_dto import LoginDTO
from OAuth2.domain.exceptions.auth_exceptions import InactiveUserException, InvalidCredentialsException
from OAuth2.domain.ports.user_repository import UserRepository
from OAuth2.domain.ports.password_hasher import PasswordHasher
from OAuth2.domain.ports.mfa_repository import MFARepository
from OAuth2.domain.ports.notification_service import NotificationService
from OAuth2.domain.ports.token_provider import TokenProvider


@dataclass
class LoginResult:
    mfa_required: bool
    message: str
    access_token: str | None = None
    refresh_token: str | None = None
    email: str | None = None
    user: dict | None = None


class LoginUserUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        password_hasher,
        mfa_repository,
        notification_service,
        token_provider,
    ):
        self.user_repository = user_repository
        self.password_hasher = password_hasher
        self.mfa_repository = mfa_repository
        self.notification_service = notification_service
        self.token_provider = token_provider

    def execute(self, dto: LoginDTO):
        email = dto.email
        password = dto.password

        user = self.user_repository.find_by_email(email)
        if not user:
            raise InvalidCredentialsException("Credenciales inválidas")

        if not self.password_hasher.verify(password, user.password_hash):
            raise InvalidCredentialsException("Credenciales inválidas")

        if not user.is_active:
            raise InactiveUserException("Usuario inactivo")

        self.user_repository.update_last_login(user.id)

        if user.mfa_enabled:
            code = "123456"  # luego lo reemplazas por generación real
            self.notification_service.send_mfa_code(user.email, code)

            return AuthResponseDTO(
                message="Código MFA enviado al correo",
                mfa_required=True,
                email=user.email,
            )

        roles = ["user"]
        access_token = self.token_provider.generate_access_token(user.id, user.email, roles)
        refresh_token = self.token_provider.generate_refresh_token(user.id)

        return AuthResponseDTO(
            message="Login exitoso",
            mfa_required=False,
            access_token=access_token,
            refresh_token=refresh_token,
            user=AuthUserDTO(
                id=user.id,
                email=user.email,
                nombres=user.nombres,
                apellidos=user.apellidos,
                roles=roles,
            ),
        )