from rest_framework import routers
from core.user.viewsets import UserViewset

router = routers.SimpleRouter()

# User Router
router.register(r'user', UserViewset, basename='user')

urlpatterns = [
    # *router.urls is unpacking the list of URL patterns.
    *router.urls
]