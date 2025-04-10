from .models import User
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import SignupSerializer
from .serializers import PasswordResetRequestSerializer, PasswordResetVerifySerializer
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.
class SignupAPIView(APIView):

    permission_classes = []

    def post(self, request):
        password = request.POST.get("password", None)
        confirm_password = request.POST.get("confirm_password", None)
        if password == confirm_password:
            serializer = SignupSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            user = serializer.save()
            data = serializer.data
            response = status.HTTP_201_CREATED

            refresh = RefreshToken.for_user(user)
            access = refresh.access_token

            response_data = {
                "success": True,
                "status": status.HTTP_201_CREATED,
                "message": "User created successfully.",
                "data": data,
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(access),
                },
            }
        else:
            data = ""
            raise ValidationError(
                {"password_mismatch": "Password fields didn not match."}
            )
        return Response(response_data, status=response)


# password reset otp
class PasswordResetRequestAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            return Response(
                {"message": "OTP sent to email."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetVerifyAPIView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = PasswordResetVerifySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Password reset successful."}, status=status.HTTP_200_OK
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
