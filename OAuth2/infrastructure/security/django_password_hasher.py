# OAuth2/infrastructure/security/django_password_hasher.py
from django.contrib.auth.hashers import make_password, check_password
from OAuth2.domain.ports.password_hasher import PasswordHasher


class DjangoPasswordHasher(PasswordHasher):
    def hash(self, plain_password: str) -> str:
        return make_password(plain_password)

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return check_password(plain_password, hashed_password)