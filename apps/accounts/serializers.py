from rest_framework import serializers
from django.contrib.auth.models import User
from apps.accounts.models import UserProfile

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['state', 'district', 'age', 'occupation', 'income_range', 'preferred_language', 'user_interests']

class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'is_staff', 'profile']

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    state = serializers.CharField(required=False, default='Andhra Pradesh')
    district = serializers.CharField(required=False, allow_blank=True, default='')
    age = serializers.IntegerField(required=False, allow_null=True)
    occupation = serializers.CharField(required=False, default='general_public')
    income_range = serializers.CharField(required=False, allow_blank=True, default='')
    preferred_language = serializers.CharField(required=False, default='en')

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'first_name', 'last_name', 'state', 'district', 'age', 'occupation', 'income_range', 'preferred_language']

    def create(self, validated_data):
        profile_data = {
            'state': validated_data.pop('state', 'Andhra Pradesh'),
            'district': validated_data.pop('district', ''),
            'age': validated_data.pop('age', None),
            'occupation': validated_data.pop('occupation', 'general_public'),
            'income_range': validated_data.pop('income_range', ''),
            'preferred_language': validated_data.pop('preferred_language', 'en'),
        }
        password = validated_data.pop('password')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()
        UserProfile.objects.create(user=user, **profile_data)
        return user
