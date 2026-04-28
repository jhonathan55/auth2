from dataclasses import dataclass


@dataclass(frozen=True)
class VerifyMFADTO:
    email: str
    code: str
    purpose: str = "LOGIN"