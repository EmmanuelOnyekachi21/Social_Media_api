from core.abstract.viewsets import AbstractViewSet
from core.auth.permissions import UserPermission
from core.post.models import Post
from core.post.serializers import PostSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action


class PostViewSet(AbstractViewSet):
    http_method_names = ['get', 'post', 'put', 'delete']
    permission_classes = (UserPermission,)
    serializer_class = PostSerializer
    
    def get_queryset(self):
        return Post.objects.all()
    
    def get_object(self):
        obj = Post.objects.get_object_by_public_id(
            self.kwargs['pk']
        )
        self.check_object_permissions(self.request, obj)
        return obj
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            serializer.data, 
            status=status.HTTP_201_CREATED
        )
    
    @action(methods=['post'], detail=True)
    def like(self, request, *args, **kwargs):
        """
        POST /posts/{pk}/like/
        Custom action to like a post.
        Uses @action decorator with detail=True because
        it targets a single object (e.g., post with id=5).
        """
        post = self.get_object() # Retrieves the Post to like
        user = self.request.user
        user.like(post)
        serializer = self.get_serializer(post)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
    
    @action(methods=['post'], detail=True)
    def remove_like(self, request, *args, **kwargs):
        """
        POST /posts/{pk}/remove_like/
        Custom action to unlike (remove like from) a post.
        """
        post = self.get_object()
        user = self.request.user
        user.remove_like(post)
        serializer = self.get_serializer(post)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )
        
        
