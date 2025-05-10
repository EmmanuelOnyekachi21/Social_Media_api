from rest_framework import serializers
from core.user.serializer import UserSerializer
from core.user.models import User
from django.contrib.auth.password_validation import validate_password


class RegisterSerializer(UserSerializer):
    """
    Registration serializer for request and user creation.
    """
    # Making sure that the password is at least 8 characters long,
    # and no longer than 128 characters.  Password can't be read by user also.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True,
        required=True
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True
    )
    
    class Meta:
        model = User
        fields = [
            'id', 'bio', 'avatar', 'email', 'username',
            'first_name', 'last_name', 'password', 'confirm_password'
        ]
    
    def validate(self, attrs):
        # Check if password matches
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError(
                {'confirm_password': 'Passwords doesn\'t match'}
            )
        
        # Validate password strength
        validate_password(attrs['password'])

        return attrs
    
    def create(self, validated_data):
        # Remove the confirm_password field.
        validated_data.pop('confirm_password')
        # Use the `create_user ` method we wrote earlier for the UserManager
        # to create a new user.
        return User.objects.create_user(**validated_data)