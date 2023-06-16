import pytest
from rest_framework.reverse import reverse
from book.views import Books


@pytest.fixture()
def auth_token(client, django_user_model):
    user_data = {
        "username": "lalu123",
        "password": "lalu12345",
        "first_name": "vasu",
        "last_name": "kv",
        "email": "ksam071@gmail.com",
        "phone": 756848777,
        "location": "Delhi",
        "is_verified": True

    }

    user = django_user_model.objects.create_user(**user_data)
    user.is_superuser = True
    user.save()

    return user.auth_token


class TestBook:

    @pytest.mark.django_db
    def test_post_book_successful(self, client, django_user_model, auth_token):
        """Test for post book"""
        book_add = {
            "author": "Ram",
            "title": "My Java",
            "price": 500,
            "quantity": 40

        }

        url = reverse('book-list')
        response = client.post(url, book_add, HTTP_AUTHORIZATION=auth_token, content_type='application/json')
        print(response.data)
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_post_book_unsuccessful(self, client, django_user_model, auth_token):
        """Test for post book fail"""
        book_add = {
            "author": "Ram",
            "title": "My Java",
            "price": 500,
            "quantity": ""

        }

        url = reverse('book-list')
        response = client.post(url, book_add, HTTP_AUTHORIZATION=auth_token, content_type='application/json')
        print(response.data)
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_get_book_successful(self, client, django_user_model, auth_token):
        """Test for get book success"""
        token = auth_token
        book_add = {
            "author": "Ram",
            "title": "My Java",
            "price": 500,
            "quantity": ""
        }
        url = reverse('book-list')
        response = client.post(url, book_add, HTTP_AUTHORIZATION=token, content_type='application/json')
        url = reverse('book-list')
        response = client.get(url, HTTP_AUTHORIZATION=token, content_type='application/json')
        assert response.status_code == 202

    @pytest.mark.django_db
    def test_get_book_unsuccessful(self, client, django_user_model, auth_token):
        """Test for get book fail"""
        token = auth_token
        book_add = {
            "author": "Ram",
            "title": "My Java",
            "price": 500,
            "quantity": ""
        }
        url = reverse('book-list')
        response = client.post(url, book_add, HTTP_AUTHORIZATION=token, content_type='application/json')
        url = reverse('book-list')
        response = client.get(url, content_type='application/json')
        assert response.status_code == 403



    @pytest.mark.django_db
    def test_delete_book_successful(self, client, django_user_model, auth_token):
        """Test for delete book"""
        post_book = {
            "author": "Ram",
            "title": "My Java",
            "price": 500,
            "quantity": 40
        }
        url = reverse("book-list")
        response = client.post(url, post_book, HTTP_AUTHORIZATION=auth_token, content_type='application/json')
        book_id = response.data['data']["id"]
        url = reverse('book-detail', args=[book_id])
        response = client.delete(url, HTTP_AUTHORIZATION=auth_token, content_type='application/json')
        assert response.status_code == 200


    @pytest.mark.django_db
    def test_delete_book_unsuccessful(self, client, django_user_model, auth_token):
        """Test for delete book fail"""
        post_book = {
            "author": "Ram",
            "title": "My Java",
            "price": 500,
            "quantity": 40
        }
        url = reverse("book-list")
        response = client.post(url, post_book, HTTP_AUTHORIZATION=auth_token, content_type='application/json')
        book_id = response.data['data']
        url = reverse('book-detail', args=[book_id])
        response = client.delete(url, HTTP_AUTHORIZATION=auth_token, content_type='application/json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_update_book_successful(self, client, django_user_model, auth_token):
        """Test for update book"""
        token = auth_token
        post_book = {
            "author": "Ram",
            "title": "My Java",
            "price": 500,
            "quantity": 40
        }
        url = reverse('book-list')
        response = client.post(url, post_book, HTTP_AUTHORIZATION=token, content_type='application/json')
        book_id = response.data["data"]["id"]
        update_book = {
            "author": "Ram",
            "title": "My Python",
            "price": 500,
            "quantity": 40
        }
        url = reverse('book-detail', args=[book_id])
        response = client.put(url, update_book, HTTP_AUTHORIZATION=token, content_type='application/json')
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_update_book_unsuccessful(self, client, django_user_model, auth_token):
        """Test for update book fail"""
        token = auth_token
        post_book = {
            "author": "Ram",
            "title": "My Java",
            "price": 500,
            "quantity": 40
        }
        url = reverse('book-list')
        response = client.post(url, post_book, HTTP_AUTHORIZATION=token, content_type='application/json')
        book_id = response.data["data"]
        update_book = {
            "author": "Ram",
            "title": "My Python",
            "price": 500,
            "quantity": 40
        }
        url = reverse('book-detail', args=[book_id])
        response = client.put(url, update_book, HTTP_AUTHORIZATION=token, content_type='application/json')
        assert response.status_code == 400
