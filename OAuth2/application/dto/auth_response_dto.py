from dataclasses import dataclass
from typing import Optional


@dataclass(frozen=True)
class AuthUserDTO:
    id: int
    email: str
    nombres: str
    apellidos: str
    roles: list[str]


@dataclass(frozen=True)
class AuthResponseDTO:
    message: str
    mfa_required: bool
    user: Optional[AuthUserDTO] = None
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None
    email: Optional[str] = None