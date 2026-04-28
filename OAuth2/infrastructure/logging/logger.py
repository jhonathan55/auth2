from OAuth2.infrastructure.logging.logger_service import LoggerService


def get_logger(name: str) -> LoggerService:
    return LoggerService(name)