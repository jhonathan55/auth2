from typing import Optional

from OAuth2.domain.entities.mfa_challenge import MFAChallenge as MFAChallengeEntity
from OAuth2.domain.ports.mfa_repository import MFARepository
from OAuth2.infrastructure.persistence.django_models import MFAChallenge as MFAChallengeORM
from OAuth2.infrastructure.logging.logger import get_logger


logger = get_logger(__name__)


class DjangoMFARepository(MFARepository):
    def save(self, challenge: MFAChallengeEntity) -> MFAChallengeEntity:
        logger.debug(
            "Persistiendo desafío MFA",
            event="mfa_save",
                extra_data={
                    "user_id": challenge.user_id,
                    "purpose": challenge.purpose,
                },
        )

        obj = MFAChallengeORM.objects.create(
            id=challenge.id,
            user_id=challenge.user_id,
            code_hash=challenge.code_hash,
            channel=challenge.channel,
            purpose=challenge.purpose,
            expires_at=challenge.expires_at,
            consumed_at=challenge.consumed_at,
            attempts=challenge.attempts,
            max_attempts=challenge.max_attempts,
            created_at=challenge.created_at,
        )

        return self._to_entity(obj)

    def find_active_by_user_and_purpose(
        self,
        user_id: int,
        purpose: str
    ) -> Optional[MFAChallengeEntity]:
        obj = (
            MFAChallengeORM.objects.filter(
                user_id=user_id,
                purpose=purpose,
                consumed_at__isnull=True,
            )
            .order_by("-created_at")
            .first()
        )

        if not obj:
            logger.info("No se encontró desafío MFA activo", extra={
                "event": "mfa_not_found",
                "user_id": user_id,
                "purpose": purpose,
            })
            return None

        return self._to_entity(obj)

    def update(self, challenge: MFAChallengeEntity) -> None:
        logger.debug("Actualizando desafío MFA", extra={
            "event": "mfa_update",
            "challenge_id": str(challenge.id),
            "attempts": challenge.attempts,
        })

        MFAChallengeORM.objects.filter(id=challenge.id).update(
            consumed_at=challenge.consumed_at,
            attempts=challenge.attempts,
            expires_at=challenge.expires_at,
            max_attempts=challenge.max_attempts,
        )

    @staticmethod
    def _to_entity(obj: MFAChallengeORM) -> MFAChallengeEntity:
        return MFAChallengeEntity(
            id=obj.id,
            user_id=obj.user_id,
            code_hash=obj.code_hash,
            channel=obj.channel,
            purpose=obj.purpose,
            expires_at=obj.expires_at,
            consumed_at=obj.consumed_at,
            attempts=obj.attempts,
            max_attempts=obj.max_attempts,
            created_at=obj.created_at,
        )