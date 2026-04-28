# OAuth2/infrastructure/security/jwt_token_provider.py
import jwt
from datetime import datetime, timedelta
from django.conf import settings
from OAuth2.domain.ports.token_provider import TokenProvider


class JwtTokenProvider(TokenProvider):
    def generate_access_token(self, user_id: int, email: str, roles: list[str]) -> str:
        payload = {
            "sub": str(user_id),
            "email": email,
            "roles": roles,
            "type": "access",
            "exp": datetime.utcnow() + timedelta(hours=1),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")

    def generate_refresh_token(self, user_id: int) -> str:
        payload = {
            "sub": str(user_id),
            "type": "refresh",
            "exp": datetime.utcnow() + timedelta(days=7),
        }
        return jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")