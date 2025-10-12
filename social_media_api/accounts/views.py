from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser

from .serializers import RegisterSerializer, UserSerializer, LoginSerializer
from .models import User


# 🧩 Registration view (supports JSON + multipart/form-data)
class RegisterAPIView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser, MultiPartParser, FormParser]  # ✅ accept both JSON and form data

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # Create or retrieve auth token
        token, _ = Token.objects.get_or_create(user=user)

        # Prepare response data
        data = UserSerializer(user, context={'request': request}).data
        data['token'] = token.key
        return Response(data, status=status.HTTP_201_CREATED)


# 🔐 Login view (returns token)
class LoginAPIView(APIView):
    permission_classes = [permissions.AllowAny]
    parser_classes = [JSONParser]  # Login always expects JSON

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        data = UserSerializer(user, context={'request': request}).data
        data['token'] = token.key
        return Response(data)


# 👤 Profile view (retrieve/update your own profile)
class ProfileAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [JSONParser, MultiPartParser, FormParser]  # ✅ handle both JSON and file uploads

    def get_object(self):
        return self.request.user
