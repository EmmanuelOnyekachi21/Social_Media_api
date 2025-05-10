from rest_framework import routers
from core.user.viewsets import UserViewset
from core.auth.viewsets.register import RegisterViewSet

router = routers.SimpleRouter()

# User Router
router.register(r'user', UserViewset, basename='user')

# Auth Router
router.register(r'auth/register', RegisterViewSet, basename='auth-register')

urlpatterns = [
    # *router.urls is unpacking the list of URL patterns.
    *router.urls
]