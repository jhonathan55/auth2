from abc import ABC, abstractmethod


class NotificationService(ABC):
    @abstractmethod
    def send_mfa_code(self, to_email: str, code: str) -> None:
        pass