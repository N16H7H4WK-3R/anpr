from rest_framework import viewsets, status, generics
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserSerializer, CustomTokenObtainPairSerializer
from rest_framework.decorators import action
from .helpers import get_tokens_for_user

User = get_user_model()


# API View to retrieve user details by pk
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'pk'

    # Override the retrieve method to customize the response
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        # Get the serialized data
        data = serializer.data
        return Response(data)


# Custom Token Obtain View for Login


class CustomTokenObtainPairView(APIView):
    permission_classes = [AllowAny]
    serializer_class = CustomTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            tokens = get_tokens_for_user(user)
            return Response({
                'username': user.username,
                'role': user.role,
                'id': user.id,
                **tokens
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

# Signup API


class SignupView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = request.data
        role = data.get('role', User.MEMBER)
        serializer = UserSerializer(data=data)

        if serializer.is_valid():
            # Check if the role is SuperUser and ensure the requesting user is a superuser
            if role == User.SUPERUSER:
                if not request.user.is_superuser:
                    return Response({"detail": "Only superusers can create another superuser"},
                                    status=status.HTTP_403_FORBIDDEN)

            if role == User.SUB_ADMIN:
                if not request.user.is_superuser:
                    return Response({"detail": "Only superusers can create a Sub Admin"},
                                    status=status.HTTP_403_FORBIDDEN)

            user = serializer.save()
            user.set_password(data['password'])

            # Set is_superuser and is_staff if creating a superuser
            if role == User.SUPERUSER:
                user.is_superuser = True
                user.is_staff = True

            user.role = role
            user.save()

            return Response({
                "message": "User created successfully",
            }, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# User Profile API

class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request):
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request):
        user = request.user
        user.delete()
        return Response({"message": "User deleted successfully"}, status=status.HTTP_204_NO_CONTENT)


# Logout API


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Get the refresh token from the request
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)

            # Blacklist the token (add it to the blacklist)
            token.blacklist()

            return Response({"message": "Successfully logged out"}, status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# Viewset to get all users

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    @action(detail=False, methods=['get'])
    def sub_admins(self, request):
        queryset = User.objects.filter(role=User.SUB_ADMIN)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def members(self, request):
        queryset = User.objects.filter(role=User.MEMBER)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)
