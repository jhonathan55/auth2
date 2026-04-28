from abc import ABC, abstractmethod
from typing import Optional

from OAuth2.domain.entities.mfa_challenge import MFAChallenge


class MFARepository(ABC):
    @abstractmethod
    def save(self, challenge: MFAChallenge) -> MFAChallenge:
        pass

    @abstractmethod
    def find_active_by_user_and_purpose(self, user_id: int, purpose: str) -> Optional[MFAChallenge]:
        pass

    @abstractmethod
    def update(self, challenge: MFAChallenge) -> None:
        pass