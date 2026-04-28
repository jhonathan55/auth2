from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from uuid import UUID


@dataclass
class MFAChallenge:
    id: UUID
    user_id: int
    code_hash: str
    channel: str
    purpose: str
    expires_at: datetime
    consumed_at: Optional[datetime]
    attempts: int
    max_attempts: int
    created_at: datetime