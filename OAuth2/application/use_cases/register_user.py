# OAuth2/application/use_cases/register_user.py
from OAuth2.domain.entities.user import User as UserEntity
from OAuth2.domain.ports.user_repository import UserRepository
from OAuth2.domain.ports.password_hasher import PasswordHasher


class RegisterUserUseCase:
    def __init__(self, user_repository: UserRepository, password_hasher: PasswordHasher):
        self.user_repository = user_repository
        self.password_hasher = password_hasher

    def execute(self, nombres: str, apellidos: str, email: str, password: str) -> UserEntity:
        existing = self.user_repository.find_by_email(email)
        if existing:
            raise ValueError("El correo ya está registrado")

        user = UserEntity(
            id=None,
            nombres=nombres,
            apellidos=apellidos,
            email=email,
            password_hash=self.password_hasher.hash(password),
            is_active=True,
            is_staff=False,
            is_email_verified=False,
            mfa_enabled=False,
        )

        return self.user_repository.save(user)