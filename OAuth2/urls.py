from django.urls import path
from .views import (
    ChangePasswordWithRecoveryView,
    LoginView,
    RegisterView,
    RequestPasswordRecoveryView,
    VerifyMFAView,
    VerifyPasswordRecoveryCodeView,
)

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("verify-mfa/", VerifyMFAView.as_view(), name="verify-mfa"),
    path("password-recovery/request-code/", RequestPasswordRecoveryView.as_view(), name="password-recovery-request-code"),
    path("password-recovery/verify-code/", VerifyPasswordRecoveryCodeView.as_view(), name="password-recovery-verify-code"),
    path("password-recovery/change-password/", ChangePasswordWithRecoveryView.as_view(), name="password-recovery-change-password"),
]
