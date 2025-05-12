from rest_framework import status
import pytest
from core.fixtures.user import user
from core.fixtures.post import post


class TestViewSet:
    endpoint = '/api/post/'

    def test_list(self, post, user, client):
        client.force_authenticate(user=user)
        response = client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['count'] == 1
    
    def test_retrieve(self, client, user, post):
        client.force_authenticate(user=user)
        response = client.get(self.endpoint + str(post.public_id) + '/')
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == post.public_id.hex
        assert response.data['body'] == post.body
        assert response.data['author']['id'] == user.public_id.hex
    
    def test_create(self, client, post, user):
        client.force_authenticate(user=user)
        data = {
            "author":user.public_id.hex,
            "body": "A test post",
        }
        print(data)
        response = client.post(
            self.endpoint,
            data
        )
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['body'] == data['body']
        assert response.data['author']['id'] == user.public_id.hex
    
    def test_update(self, client, user, post):
        client.force_authenticate(user=user)
        data = {
            "body": "Edited",
            "author": user.public_id.hex
        }
        response = client.put(
            self.endpoint + str(post.public_id) + '/',
            data
        )
        assert response.status_code == status.HTTP_200_OK
        assert response.data['body'] == data['body']
        assert response.data['edited'] == True
    
    def test_delete(self, post, user, client):
        client.force_authenticate(user=user)
        response = client.delete(
            self.endpoint + str(post.public_id) + '/'
        )
        assert response.status_code == status.HTTP_204_NO_CONTENT

    def test_list_anonymous(self, client, post):
        response = client.get(self.endpoint)
        assert response.status_code == status.HTTP_200_OK
        assert response.data["count"] == 1
    
    def test_retrieve_anonymous(self, client, post):
        response = client.get(self.endpoint + str(post.public_id) + "/")
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id'] == post.public_id.hex
        assert response.data['body'] == post.body
        assert response.data['author']['id'] == post.author.public_id.hex
    
    def test_create_anonymous(self, client, user, post):
        data = {
            "body": "Test Post Body",
            "author": "test_user"
        }
        reponse = client.post(self.endpoint, data)
        assert reponse.status_code == status.HTTP_401_UNAUTHORIZED
    
    def test_update_anonymous(self, client, post):
        data = {
            "body": "Test Post Body",
            "author": "test_user"
        }
        response = client.put(self.endpoint + str(post.public_id) + "/", data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_delete_anonymous(self, client, post):
        response = client.delete(self.endpoint + str(post.public_id) + "/")
        assert response.status_code == status.HTTP_401_UNAUTHORIZED
