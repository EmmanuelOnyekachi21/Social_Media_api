import pytest
from core.fixtures.user import user
from core.fixtures.post import post
from core.comment.models import Comment


@pytest.mark.django_db
def test_comment(post, user):
    comment = Comment.objects.create(
        author=user,
        post=post,
        body='Test Comment body'
    )
    assert comment.author == user
    assert comment.post == post
    assert comment.body == 'Test Comment body'
