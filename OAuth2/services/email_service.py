from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
import logging


logger = logging.getLogger("OAuth2")


def send_mfa_email(user, code):
    subject = "Tu código de verificación"
    from_email = getattr(
        settings,
        "DEFAULT_FROM_EMAIL",
        getattr(settings, "EMAIL_HOST_USER", "no-reply@oauth2.local"),
    )
    to = [user.email]

    try:
        html_content = render_to_string("emails/mfa_code.html", {
            "user": user,
            "code": code,
        })
    except Exception:
        html_content = f"""
        <html>
            <body>
                <h2>Verificación de acceso</h2>
                <p>Hola {user.nombres},</p>
                <p>Tu código es: <strong>{code}</strong></p>
                <p>Expira en 5 minutos.</p>
            </body>
        </html>
        """

    text_content = f"Hola {user.nombres}, tu código de verificación es: {code}"

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    sent_count = msg.send()
    logger.info(
        "MFA email sent",
        extra={"event": "mfa_email_sent", "to": user.email, "sent_count": sent_count},
    )


def send_password_reset_email(user, code):
    subject = "Recuperación de contraseña"
    from_email = getattr(
        settings,
        "DEFAULT_FROM_EMAIL",
        getattr(settings, "EMAIL_HOST_USER", "no-reply@oauth2.local"),
    )
    to = [user.email]

    html_content = f"""
    <html>
        <body>
            <h2>Recuperación de contraseña</h2>
            <p>Hola {user.nombres},</p>
            <p>Usa este código para validar tu identidad:</p>
            <p><strong>{code}</strong></p>
            <p>Expira en 10 minutos y solo puede usarse una vez.</p>
        </body>
    </html>
    """
    text_content = (
        f"Hola {user.nombres}, usa este código para recuperar tu contraseña: {code}. "
        "Expira en 10 minutos y solo puede usarse una vez."
    )

    msg = EmailMultiAlternatives(subject, text_content, from_email, to)
    msg.attach_alternative(html_content, "text/html")
    sent_count = msg.send()
    logger.info(
        "Password recovery email sent",
        extra={"event": "password_recovery_email_sent", "to": user.email, "sent_count": sent_count},
    )
