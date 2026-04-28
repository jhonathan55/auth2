from typing import Optional

from django.utils import timezone

from OAuth2.domain.entities.user import User as UserEntity
from OAuth2.domain.ports.user_repository import UserRepository
from OAuth2.infrastructure.persistence.django_models import AppUser as AppUserORM
from OAuth2.infrastructure.logging.logger import get_logger


logger = get_logger(__name__)


class DjangoUserRepository(UserRepository):
    def save(self, user: UserEntity) -> UserEntity:
        logger.debug("Persistiendo usuario", extra={
            "event": "user_save",
            "email": user.email,
        })

        obj = AppUserORM.objects.create(
            nombres=user.nombres,
            apellidos=user.apellidos,
            email=user.email,
            password=user.password_hash,
            is_active=user.is_active,
            is_staff=user.is_staff,
            is_email_verified=user.is_email_verified,
            mfa_enabled=user.mfa_enabled,
        )

        return self._to_entity(obj)

    def find_by_email(self, email: str) -> Optional[UserEntity]:
        obj = AppUserORM.objects.filter(email=email).first()
        if not obj:
            logger.info(
                "Usuario no encontrado por email",
                event="user_not_found_by_email",
                extra_data={"email": email},
            )
            return None

        return self._to_entity(obj)

    def find_by_id(self, user_id: int) -> Optional[UserEntity]:
        obj = AppUserORM.objects.filter(id=user_id).first()
        if not obj: 
            logger.info(
                "Usuario no encontrado por ID",
                event="user_not_found_by_id",
                extra_data={"user_id": user_id},
            )
            return None

        return self._to_entity(obj)

    def update_last_login(self, user_id: int) -> None:
        logger.debug(
            "Actualizando último login del usuario",
            event="update_last_login",
            extra_data={"user_id": user_id},
        )

        AppUserORM.objects.filter(id=user_id).update(last_login_at=timezone.now())

    @staticmethod
    def _to_entity(obj: AppUserORM) -> UserEntity:
        return UserEntity(
            id=obj.id,
            nombres=obj.nombres,
            apellidos=obj.apellidos,
            email=obj.email,
            password_hash=obj.password,
            is_active=obj.is_active,
            is_staff=obj.is_staff,
            is_email_verified=obj.is_email_verified,
            mfa_enabled=obj.mfa_enabled,
            last_login_at=obj.last_login_at,
        )