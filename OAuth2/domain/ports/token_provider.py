# OAuth2/domain/ports/token_provider.py
from abc import ABC, abstractmethod


class TokenProvider(ABC):
    @abstractmethod
    def generate_access_token(self, user_id: int, email: str, roles: list[str]) -> str:
        pass

    @abstractmethod
    def generate_refresh_token(self, user_id: int) -> str:
        pass