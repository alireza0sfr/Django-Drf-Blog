import pytest
from django.urls import reverse

from tests.base import BaseTest
from factories.blog import PostFactory
from factories.accounts import UserFactory

class TestBlogAPI(BaseTest):
    
    list_url = reverse('posts-list')

    @pytest.mark.django_db
    def test_create_object_response_401(self):

        # Arrange

        # Act
        response = self.api_client.post(self.list_url)
        
        # Assert
        assert response.status_code == 401

    @pytest.mark.django_db
    def test_create_object_response_201(self):

        # Arrange
        post = PostFactory.build()
        
        # Act
        self.api_client.force_authenticate(UserFactory())
        response = self.api_client.post(self.list_url, data={
            'title': post.title,
            'content': post.content,
            'status': post.status,
        })

        # Assert
        assert response.data.get('title') == post.title
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_get_object_response_200(self):

        # Arrange
        post = PostFactory()
        
        # Act
        self.api_client.force_authenticate(UserFactory())
        response = self.api_client.get(reverse('posts-detail', kwargs={'pk': post.pk}))

        # Assert
        assert response.data.get('title') == post.title
        assert response.data.get('id') == str(post.id)
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_put_object_response_200(self):

        # Arrange
        post = PostFactory()
        
        # Act
        self.api_client.force_authenticate(UserFactory())
        response = self.api_client.put(reverse('posts-detail', kwargs={'pk': post.pk}), 
                                        data={
                                            'title': 'updated-title'
                                        })

        # Assert
        assert response.data.get('title') == 'updated-title'
        assert response.data.get('id') == str(post.id)
        assert response.status_code == 200


    @pytest.mark.django_db
    def test_list_object_response_200(self):

        # Arrange
        count = 3
        post = PostFactory.create_batch(count)
        
        # Act
        self.api_client.force_authenticate(UserFactory())
        response = self.api_client.get(self.list_url)

        # Assert
        assert response.data.get('count') == count
        assert response.status_code == 200
        