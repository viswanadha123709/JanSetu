from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from apps.accounts.serializers import UserSerializer, RegisterSerializer
from apps.accounts.models import UserProfile

class RegisterView(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response(UserSerializer(user).data)
        return Response({'error': 'Invalid username or password.'}, status=status.HTTP_401_UNAUTHORIZED)

class LogoutView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'Logged out successfully.'})

class ProfileView(APIView):
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'authenticated': False})
        return Response({
            'authenticated': True,
            'user': UserSerializer(request.user).data
        })

    def put(self, request):
        if not request.user.is_authenticated:
            return Response({'error': 'Authentication required.'}, status=status.HTTP_401_UNAUTHORIZED)
        
        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        data = request.data
        if 'state' in data: profile.state = data['state']
        if 'district' in data: profile.district = data['district']
        if 'age' in data: profile.age = data['age']
        if 'occupation' in data: profile.occupation = data['occupation']
        if 'income_range' in data: profile.income_range = data['income_range']
        if 'preferred_language' in data: profile.preferred_language = data['preferred_language']
        if 'user_interests' in data: profile.user_interests = data['user_interests']
        profile.save()
        
        return Response(UserSerializer(request.user).data)
