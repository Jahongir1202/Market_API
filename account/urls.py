from django.urls import path
from .views import RegisterView, ChangePasswordView, ResetPasswordRequestView, ResetPasswordConfirmView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('change-password/', ChangePasswordView.as_view(), name='change_password'),
    path('password-reset/', ResetPasswordRequestView.as_view(), name='password_reset'),
    path('reset/<uidb64>/<token>/', ResetPasswordConfirmView.as_view(), name='password_reset_confirm'),

]
