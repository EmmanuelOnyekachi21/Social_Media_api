from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from core.abstract.serializers import AbstractSerializer
from core.user.serializer import UserSerializer
from core.user.models import User
from core.post.models import Post
from core.comment.models import Comment


class CommentSerializer(AbstractSerializer):
    author = serializers.SlugRelatedField(
        queryset=User.objects.all(), slug_field='public_id'
    )
    post = serializers.SlugRelatedField(
        queryset=Post.objects.all(), slug_field='public_id'
    )
    
    def to_representation(self, instance):
        rep = super().to_representation(instance)
        author = User.objects.get_object_by_public_id(rep['author'])
        rep['author'] = UserSerializer(author).data
        return rep
    
    def validate_post(self, value):
        """
        self.instance is set only during update requests (PUT/PATCH).

        During update, this method forces the post value to stay the same (i.e., self.instance.post).

        During creation (POST), self.instance is None, so we accept the value normally.
        """
        # If we're updating an existing comment (PUT/PATCH), 
        # don't allow the post to change
        if self.instance:
            return self.instance.post
        # If it's a create (POST), accept the value from user
        return value
    
    def update(self, instance, validated_data):
        if not instance.edited:
            validated_data['edited'] = True
        return super().update(instance, validated_data)
    
    
    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'author', 'body', 'edited', 'created', 'updated'
        ]
        read_only_fields = ['edited']

