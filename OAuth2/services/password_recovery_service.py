from datetime import timedelta

from django.contrib.auth.hashers import check_password, make_password
from django.utils import timezone

from OAuth2.models import AppUser, MFAChallenge

from .mfa_service import generate_6_digit_code


PASSWORD_RESET_PURPOSE = "RESET_PASSWORD"
PASSWORD_RESET_EXPIRATION_MINUTES = 10


class PasswordRecoveryError(Exception):
    pass


def create_password_reset_challenge(user: AppUser):
    now = timezone.now()
    expires_at = now + timedelta(minutes=PASSWORD_RESET_EXPIRATION_MINUTES)
    code = generate_6_digit_code()

    MFAChallenge.objects.filter(
        user=user,
        purpose=PASSWORD_RESET_PURPOSE,
        consumed_at__isnull=True,
    ).update(consumed_at=now)

    challenge = MFAChallenge.objects.create(
        user=user,
        code_hash=make_password(code),
        purpose=PASSWORD_RESET_PURPOSE,
        expires_at=expires_at,
        max_attempts=5,
    )

    return challenge, code


def verify_password_reset_code(email: str, code: str, lock: bool = False):
    try:
        user = AppUser.objects.get(
            email=email,
            is_active=True,
        )
        challenges = MFAChallenge.objects

        if lock:
            challenges = challenges.select_for_update()

        challenge = challenges.filter(
            user=user,
            purpose=PASSWORD_RESET_PURPOSE,
            consumed_at__isnull=True,
        ).order_by("-created_at").first()
        if challenge is None:
            raise MFAChallenge.DoesNotExist()
    except (AppUser.DoesNotExist, MFAChallenge.DoesNotExist, ValueError):
        raise PasswordRecoveryError()

    if timezone.now() > challenge.expires_at:
        raise PasswordRecoveryError()

    if challenge.attempts >= challenge.max_attempts:
        raise PasswordRecoveryError()

    if challenge.verified_at is not None:
        return user, challenge

    if not check_password(code, challenge.code_hash):
        challenge.attempts += 1
        challenge.save(update_fields=["attempts"])
        raise PasswordRecoveryError()

    challenge.verified_at = timezone.now()
    challenge.save(update_fields=["verified_at"])

    return user, challenge


def get_verified_password_reset_challenge(email: str, lock: bool = False):
    try:
        user = AppUser.objects.get(email=email, is_active=True)
    except AppUser.DoesNotExist:
        raise PasswordRecoveryError()

    challenges = MFAChallenge.objects
    if lock:
        challenges = challenges.select_for_update()

    challenge = challenges.filter(
        user=user,
        purpose=PASSWORD_RESET_PURPOSE,
        verified_at__isnull=False,
        consumed_at__isnull=True,
    ).order_by("-verified_at", "-created_at").first()

    if challenge is None:
        raise PasswordRecoveryError()

    if timezone.now() > challenge.expires_at:
        raise PasswordRecoveryError()

    return user, challenge


def consume_password_reset_challenge(challenge: MFAChallenge):
    challenge.consumed_at = timezone.now()
    challenge.save(update_fields=["consumed_at"])
