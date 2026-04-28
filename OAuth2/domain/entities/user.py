# OAuth2/domain/entities/user.py
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: int | None
    nombres: str
    apellidos: str
    email: str
    password_hash: str
    is_active: bool
    is_staff: bool
    is_email_verified: bool
    mfa_enabled: bool
    last_login_at: Optional[datetime] = None