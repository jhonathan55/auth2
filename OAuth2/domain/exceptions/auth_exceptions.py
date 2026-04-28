class AuthDomainException(Exception):
    """Excepción base del dominio de autenticación."""


class InvalidCredentialsException(AuthDomainException):
    pass


class InactiveUserException(AuthDomainException):
    pass


class UserAlreadyExistsException(AuthDomainException):
    pass


class UserNotFoundException(AuthDomainException):
    pass


class MFAChallengeNotFoundException(AuthDomainException):
    pass


class InvalidOrExpiredMFACodeException(AuthDomainException):
    pass


class MFAAttemptsExceededException(AuthDomainException):
    pass