from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from core.auth.serializers import RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken


class RegisterViewSet(viewsets.ViewSet):
    serializer_class = RegisterSerializer
    http_method_names = ['post']
    permission_classes = (AllowAny,)

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # generates both refresh and access JWT tokens for the created user.
        # These tokens are then used for authentication.
        refresh = RefreshToken.for_user(user)        

        # Create dictionary containing the refresh and access token
        res = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        
        return Response(
            {
                "user": serializer.data,
                "refresh": res["refresh"],
                "access": res["access"]
            },
            status=status.HTTP_201_CREATED
        )
