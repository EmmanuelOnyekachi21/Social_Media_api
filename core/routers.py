from rest_framework import routers
from core.user.viewsets import UserViewset
from core.auth.viewsets import RegisterViewSet, LoginViewSet

router = routers.SimpleRouter()

# User Router
router.register(r'user', UserViewset, basename='user')

# Auth Router
router.register(r'auth/register', RegisterViewSet, basename='auth-register')
router.register(r'auth/login', LoginViewSet, basename='auth-login')

urlpatterns = [
    # *router.urls is unpacking the list of URL patterns.
    *router.urls
]
