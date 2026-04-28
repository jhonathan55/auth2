# OAuth2/domain/ports/user_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from OAuth2.domain.entities.user import User as UserEntity


class UserRepository(ABC):
    @abstractmethod
    def save(self, user: UserEntity) -> UserEntity:
        pass

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def find_by_id(self, user_id: int) -> Optional[UserEntity]:
        pass

    @abstractmethod
    def update_last_login(self, user_id: int) -> None:
        pass