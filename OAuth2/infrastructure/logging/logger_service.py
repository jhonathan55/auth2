import logging
from typing import Any


class LoggerService:
    def __init__(self, logger_name: str):
        self.logger = logging.getLogger(logger_name)

    def debug(self, message: str, event: str | None = None, extra_data: dict[str, Any] | None = None) -> None:
        self.logger.debug(message, extra=self._build_extra(event, extra_data))

    def info(self, message: str, event: str | None = None, extra_data: dict[str, Any] | None = None) -> None:
        self.logger.info(message, extra=self._build_extra(event, extra_data))

    def warning(self, message: str, event: str | None = None, extra_data: dict[str, Any] | None = None) -> None:
        self.logger.warning(message, extra=self._build_extra(event, extra_data))

    def error(self, message: str, event: str | None = None, extra_data: dict[str, Any] | None = None) -> None:
        self.logger.error(message, extra=self._build_extra(event, extra_data))

    def exception(self, message: str, event: str | None = None, extra_data: dict[str, Any] | None = None) -> None:
        self.logger.exception(message, extra=self._build_extra(event, extra_data))

    @staticmethod
    def _build_extra(event: str | None, extra_data: dict[str, Any] | None) -> dict[str, Any]:
        payload = {
            "event": event or "application_event",
        }
        if extra_data:
            payload.update(extra_data)
        return payload