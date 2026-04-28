from OAuth2.application.use_cases.login_user import LoginUserUseCase
from OAuth2.application.use_cases.register_user import RegisterUserUseCase
from OAuth2.application.use_cases.verify_mfa import VerifyMFAUseCase

from OAuth2.infrastructure.logging.logger import get_logger
from OAuth2.infrastructure.notifications.email_notification_service import EmailNotificationService
from OAuth2.infrastructure.persistence.django_mfa_repository import DjangoMFARepository
from OAuth2.infrastructure.persistence.django_user_repository import DjangoUserRepository
from OAuth2.infrastructure.security.django_password_hasher import DjangoPasswordHasher
from OAuth2.infrastructure.security.jwt_token_provider import JwtTokenProvider


class Container:
    @staticmethod
    def register_user_use_case() -> RegisterUserUseCase:
        return RegisterUserUseCase(
            user_repository=DjangoUserRepository(),
            password_hasher=DjangoPasswordHasher(),
        )

    @staticmethod
    def login_user_use_case() -> LoginUserUseCase:
        return LoginUserUseCase(
            user_repository=DjangoUserRepository(),
            password_hasher=DjangoPasswordHasher(),
            mfa_repository=DjangoMFARepository(),
            notification_service=Container.email_notification_service(),
            token_provider=JwtTokenProvider(),
        )

    @staticmethod
    def verify_mfa_use_case() -> VerifyMFAUseCase:
        return VerifyMFAUseCase(
            user_repository=DjangoUserRepository(),
            mfa_repository=DjangoMFARepository(),
            password_hasher=DjangoPasswordHasher(),
            token_provider=JwtTokenProvider(),
        )

    @staticmethod
    def logger(name: str = "OAuth2"):
        return get_logger(name)

    @staticmethod
    def email_notification_service() -> EmailNotificationService:
        return EmailNotificationService(
            logger=Container.logger("OAuth2.notifications.email")
        )