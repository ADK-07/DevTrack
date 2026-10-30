from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer

class RegisterView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        
        serializer.is_valid(raise_exception=True)  # validation
        user = serializer.save() # calls serializer.create()
        return Response(
            {
                "message": "Registration successful.",
                "user": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "email": user.email,
                    "role": user.role,
                },
            },
            status=status.HTTP_201_CREATED,
        )
        
class LoginView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        
        email = request.data.get('email', '').strip().lower()
        password =request.data.get('password', '')
        
        
        if not email or not password:
            return Response({
                "message": "Email and password are required"
            }, 
            status=status.HTTP_400_BAD_REQUEST,
            )
            
        user = authenticate(
            request,
            email=email,
            password=password
        )
        
        if user is None:
            return Response({
                "message": "Invalid email or password"
            },
            status=status.HTTP_401_UNAUTHORIZED,
            )
            
        refresh = RefreshToken.for_user(user)
        
        return Response(
            {
                "message": "Login successful.",
                "user": {
                    "id": user.id,
                    "full_name": user.full_name,
                    "email": user.email,
                    "role": user.role,
                },
                "tokens": {
                    "refresh": str(refresh),
                    "access": str(refresh.access_token),
                },
            },
            status=status.HTTP_200_OK,
        )
        
        
class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user

        return Response(
            {
                "id": user.id,
                "full_name": user.full_name,
                "email": user.email,
                "role": user.role,
            },
            status=status.HTTP_200_OK,
        )   



