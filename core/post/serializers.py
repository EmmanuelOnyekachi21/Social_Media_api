from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from core.abstract.serializers import AbstractSerializer
from core.post.models import Post
from core.user.models import User
from core.user.serializer import UserSerializer


class PostSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='public_id'
    )
    
    def validate_author(self, value):
        if self.context["request"].user != value:
            raise ValidationError(
                {
                    'author':'You can\'t create a post for another user'
                }
            )
        return value
    
    liked = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    
    def get_liked(self, obj):
        # Get the request object from the context
        request = self.context.get('request', None)
        
        # If user sending request is anonymous, return false
        if request.user.is_anonymous or request is None:
            return False
        
        # Check if user has liked this post
        return request.user.has_liked(obj)
    
    def get_likes_count(self, obj):
        return obj.liked_by.count()
    
    class Meta:
        model = Post
        fields = [
            'id', 'author', 'body', 'edited',
            'created', 'updated', 'liked', 'likes_count'
        ]
        read_only_fields = ['edited']
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = User.objects.get_object_by_public_id(rep['author'])
        rep['author'] = UserSerializer(author).data
        return rep
    
    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True
        
        instance = super().update(instance, validated_data)
        return instance
    