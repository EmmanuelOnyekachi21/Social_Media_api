from rest_framework_nested import routers
from core.user.viewsets import UserViewset
from core.auth.viewsets import RegisterViewSet, LoginViewSet, RefreshViewSet
from core.post.viewsets import PostViewSet
from core.comment.viewsets import CommentViewSet

router = routers.SimpleRouter()

# User Router
router.register(r'user', UserViewset, basename='user')

# Auth Router
router.register(r'auth/register', RegisterViewSet, basename='auth-register')
router.register(r'auth/login', LoginViewSet, basename='auth-login')
router.register(r'auth/refresh', RefreshViewSet, basename='auth-refresh')

# Post ROuter
# This is your top-level router — it handles /post/ and /post/<id>/.
router.register(r'post', PostViewSet, basename='post')

"""
router: the parent router

r'post': the parent route to nest under (/post/)

lookup='post': this means the nested URLs will include post_pk in the kwargs.

For example:

    /post/12/comment/ → the 12 will be available\
        as kwargs['post_pk'] inside CommentViewSet
"""
posts_router = routers.NestedSimpleRouter(router, r'post', lookup='post')
posts_router.register(r'comment', CommentViewSet, basename='post-comment')

urlpatterns = [
    # *router.urls is unpacking the list of URL patterns.
    *router.urls,
    *posts_router.urls
]
