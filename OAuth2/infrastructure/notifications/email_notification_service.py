from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from OAuth2.domain.ports.notification_service import NotificationService
from OAuth2.infrastructure.logging.logger_service import LoggerService


class EmailNotificationService(NotificationService):
    def __init__(self, logger: LoggerService):
        self.logger = logger

    def send_mfa_code(self, to_email: str, code: str) -> None:
        subject = "Tu código MFA"

        context = {
            "code": code,
            "expiration_minutes": 5,
        }

        html_content = render_to_string("emails/mfa_code.html", context)
        text_content = render_to_string("emails/mfa_code.txt", context)

        message = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[to_email],
        )
        message.attach_alternative(html_content, "text/html")

        self.logger.info(
            "Enviando correo MFA",
            event="send_mfa_code",
            extra_data={
                "to_email": to_email,
                "notification_type": "mfa_email",
            },
        )

        message.send(fail_silently=False)

        self.logger.info(
            "Correo MFA enviado correctamente",
            event="send_mfa_code_success",
            extra_data={
                "to_email": to_email,
            },
        )