from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.settings import api_settings
from django.contrib.auth.models import update_last_login

from core.user.serializer import UserSerializer


class LoginSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        # Call the parent class's validate method to do the usual validation
        data = super().validate(attrs)

        # Now 'self.user' is available,
        # because it's set by the parent validate() method
        # get_token generates a JWT token for the authenticated user 
        refresh = self.get_token(self.user)
        
        data['user'] = UserSerializer(self.user).data
        data['refresh'] = str(refresh)
        data['access'] = str(refresh.access_token)

        if api_settings.UPDATE_LAST_LOGIN:
            update_last_login(None, self.user)

        return data
        