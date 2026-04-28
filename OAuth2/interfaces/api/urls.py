from django.urls import path

from OAuth2.interfaces.api.views import RegisterView, LoginView, VerifyMFAView

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("verify-mfa/", VerifyMFAView.as_view(), name="verify-mfa"),
]