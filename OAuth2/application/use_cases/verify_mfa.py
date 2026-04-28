from django.utils import timezone

from OAuth2.application.dto.auth_response_dto import AuthResponseDTO, AuthUserDTO
from OAuth2.application.dto.verify_mfa_dto import VerifyMFADTO
from OAuth2.domain.exceptions.auth_exceptions import (
    UserNotFoundException,
    MFAChallengeNotFoundException,
    InvalidOrExpiredMFACodeException,
    MFAAttemptsExceededException,
)
from OAuth2.domain.ports.user_repository import UserRepository
from OAuth2.domain.ports.mfa_repository import MFARepository
from OAuth2.domain.ports.password_hasher import PasswordHasher
from OAuth2.domain.ports.token_provider import TokenProvider
from OAuth2.infrastructure.logging.logger import get_logger


logger = get_logger(__name__)


class VerifyMFAUseCase:
    def __init__(
        self,
        user_repository: UserRepository,
        mfa_repository: MFARepository,
        password_hasher: PasswordHasher,
        token_provider: TokenProvider,
    ):
        self.user_repository = user_repository
        self.mfa_repository = mfa_repository
        self.password_hasher = password_hasher
        self.token_provider = token_provider

    def execute(self, dto: VerifyMFADTO) -> AuthResponseDTO:
        logger.info("Iniciando validación MFA", extra={
            "event": "verify_mfa_start",
            "email": dto.email,
            "purpose": dto.purpose,
        })

        user = self.user_repository.find_by_email(dto.email)
        if not user:
            logger.warning("Usuario no encontrado al validar MFA", extra={
                "event": "verify_mfa_user_not_found",
                "email": dto.email,
            })
            raise UserNotFoundException("Solicitud inválida")

        challenge = self.mfa_repository.find_active_by_user_and_purpose(user.id, dto.purpose)
        if not challenge:
            raise MFAChallengeNotFoundException("No existe desafío MFA activo")

        now = timezone.now()

        if challenge.consumed_at is not None:
            raise InvalidOrExpiredMFACodeException("Código inválido o expirado")

        if challenge.expires_at < now:
            raise InvalidOrExpiredMFACodeException("Código inválido o expirado")

        if challenge.attempts >= challenge.max_attempts:
            raise MFAAttemptsExceededException("Se alcanzó el máximo de intentos permitidos")

        challenge.attempts += 1

        if not self.password_hasher.verify(dto.code, challenge.code_hash):
            self.mfa_repository.update(challenge)

            logger.warning("Código MFA inválido", extra={
                "event": "verify_mfa_invalid_code",
                "user_id": user.id,
                "attempts": challenge.attempts,
            })

            raise InvalidOrExpiredMFACodeException("Código inválido o expirado")

        challenge.consumed_at = now
        self.mfa_repository.update(challenge)

        roles = ["user"]
        access_token = self.token_provider.generate_access_token(user.id, user.email, roles)
        refresh_token = self.token_provider.generate_refresh_token(user.id)

        logger.info("MFA validado correctamente", extra={
            "event": "verify_mfa_success",
            "user_id": user.id,
        })

        return AuthResponseDTO(
            message="MFA validado correctamente",
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