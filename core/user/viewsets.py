from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets
from core.user.serializer import UserSerializer
from core.user.models import User
from core.abstract.viewsets import AbstractViewSet


class UserViewset(AbstractViewSet):
    http_method_names = ['patch', 'get']
    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer
    
    def get_queryset(self):
        if self.request.user.is_superuser:
            return User.objects.all()
        return User.objects.exclude(is_superuser=True)
    
    # Retrieve a specific user object using a public ID
    # (not the regular primary key)
    def get_object(self):
        obj = User.objects.get_object_by_public_id(self.kwargs['pk'])
        # Check if the requesting user has permission to access this
        # specific user object.
        # This activates object-level permissions if any are defined
        # in permission_classes.
        self.check_object_permissions(self.request, obj)
        return obj