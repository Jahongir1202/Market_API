from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from .serializers import RegisterSerializer, ChangePasswordSerializer, ResetPasswordSerializer
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.core.mail import send_mail
from rest_framework import generics, permissions
#Regrtratsiya va login
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer

class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    model = User
    permission_classes = (permissions.IsAuthenticated,)

    def get_object(self, queryset=None):
        return self.request.user

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get("old_password")):
                return Response({"old_password": ["Wrong password."]}, status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data.get("new_password"))
            self.object.save()
            return Response({'status': 'password set'}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ResetPasswordRequestView(generics.GenericAPIView):
    serializer_class = ResetPasswordSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.data['email']
        user = User.objects.filter(email=email).first()
        if user:
            token = PasswordResetTokenGenerator().make_token(user)
            uid = urlsafe_base64_encode(str(user.pk).encode())
            reset_link = f"http://localhost:8000/api/auth/reset/{uid}/{token}/"
            send_mail('Password Reset', f'Click to reset password: {reset_link}', 'admin@example.com', [email])
        return Response({'detail': 'Password reset link sent.'})

class ResetPasswordConfirmView(generics.GenericAPIView):
    def post(self, request, uidb64, token):
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if PasswordResetTokenGenerator().check_token(user, token):
            new_password = request.data.get('new_password')
            user.set_password(new_password)
            user.save()
            return Response({'detail': 'Password has been reset.'})
        return Response({'detail': 'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)


