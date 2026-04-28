from dataclasses import dataclass


@dataclass(frozen=True)
class RegisterDTO:
    nombres: str
    apellidos: str
    email: str
    password: str