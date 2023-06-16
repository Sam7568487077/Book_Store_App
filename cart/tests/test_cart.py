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


@pytest.fixture()
def post_book(client, django_user_model, auth_token):
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
    return book_id


class TestCart:

    @pytest.mark.django_db
    def test_create_cart_successful(self, client, django_user_model, auth_token, post_book):
        """Cart creation success"""
        token = auth_token
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_AUTHORIZATION=token, content_type='application/json')
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_create_cart_unsuccessful(self, client, django_user_model, auth_token, post_book):
        """Cart creation fail"""
        token = auth_token
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": "",
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_AUTHORIZATION=token, content_type='application/json')
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_get_cart_successful(self, client, django_user_model, auth_token):
        """get cart success"""
        token = auth_token
        url = reverse('cart-list')
        response = client.get(url, HTTP_AUTHORIZATION=token, content_type='application/json')

        assert response.status_code == 200

    @pytest.mark.django_db
    def test_get_cart_unsuccessful(self, client, django_user_model, auth_token):
        """get cart fail"""
        token = auth_token
        url = reverse('cart-list')
        response = client.get(url, content_type='application/json')

        assert response.status_code == 403

    @pytest.mark.django_db
    def test_delete_cart_successful(self, client, django_user_model, auth_token, post_book):
        """delete cart success"""
        token = auth_token
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_AUTHORIZATION=token, content_type='application/json')
        cart_id = response.data["data"]["items"][0]["cart"]
        url = reverse('cart-detail', args=[cart_id])
        response = client.delete(url, HTTP_AUTHORIZATION=token, content_type='application/json')
        assert response.status_code == 200

    @pytest.mark.django_db
    def test_delete_cart_unsuccessful(self, client, django_user_model, auth_token, post_book):
        """delete cart fail"""
        token = auth_token
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_AUTHORIZATION=token, content_type='application/json')
        cart_id = response.data["data"]["items"][0]["cart"]
        url = reverse('cart-detail', args=[cart_id])
        response = client.delete(url, content_type='application/json')
        assert response.status_code == 403


class TestOrderApi:

    @pytest.mark.django_db
    def test_post_order_successful(self, client, django_user_model, auth_token, post_book):
        '''order success'''
        token = auth_token
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_AUTHORIZATION=token, content_type='application/json')
        cart_id = response.data["data"]["id"]
        url = reverse('status-list')
        response = client.post(url, {"cart": cart_id}, HTTP_AUTHORIZATION=token, content_type='application/json')
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_post_order_unsuccessful(self, client, django_user_model, auth_token, post_book):
        '''order fail'''
        token = auth_token
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_AUTHORIZATION=token, content_type='application/json')
        cart_id = response.data["data"]["id"]
        url = reverse('status-list')
        response = client.post(url, {"cart": cart_id}, content_type='application/json')
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_get_order_successful(self, client, django_user_model, auth_token, post_book):
        """get ordered success"""
        token = auth_token
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_AUTHORIZATION=token, content_type='application/json')
        url = reverse('status-list')
        response = client.get(url, HTTP_AUTHORIZATION=token, content_type='application/json')
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_get_order_unsuccessful(self, client, django_user_model, auth_token, post_book):
        """get ordered fail"""
        token = auth_token
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_AUTHORIZATION=token, content_type='application/json')
        url = reverse('status-list')
        response = client.get(url, content_type='application/json')
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_delete_order_successful(self, client, django_user_model, auth_token, post_book):
        """order delete success"""
        token = auth_token
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_AUTHORIZATION=token, content_type='application/json')
        cart_id = response.data["data"]["id"]
        url = reverse('status-detail', args=[cart_id])
        response = client.delete(url, HTTP_AUTHORIZATION=token, content_type='application/json')
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_delete_order_unsuccessful(self, client, django_user_model, auth_token, post_book):
        """order delete fail"""
        token = auth_token
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_AUTHORIZATION=token, content_type='application/json')
        cart_id = response.data["data"]["id"]
        url = reverse('status-detail', args=[cart_id])
        response = client.delete(url, content_type='application/json')
        assert response.status_code == 403


class TestPurchase:

    @pytest.mark.django_db
    def test_post_purchase_successful(self, client, django_user_model, auth_token, post_book):
        """purchase success"""
        token = auth_token
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_AUTHORIZATION=token, content_type='application/json')
        cart_id = response.data["data"]["id"]
        url = reverse('purchase-list')
        response = client.post(url, {"cart": cart_id}, HTTP_AUTHORIZATION=token, content_type='application/json')
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_post_purchase_unsuccessful(self, client, django_user_model, auth_token, post_book):
        """purchase fail"""
        token = auth_token
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_AUTHORIZATION=token, content_type='application/json')
        cart_id = response.data["data"]["id"]
        url = reverse('purchase-list')
        response = client.post(url, {"cart": cart_id}, content_type='application/json')
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_get_purchase_successful(self, client, django_user_model, auth_token, post_book):
        """get ordered success"""
        token = auth_token
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_AUTHORIZATION=token, content_type='application/json')
        url = reverse('purchase-list')
        response = client.get(url, HTTP_AUTHORIZATION=token, content_type='application/json')
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_get_purchase_successful(self, client, django_user_model, auth_token, post_book):
        """get ordered success"""
        token = auth_token
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_AUTHORIZATION=token, content_type='application/json')
        url = reverse('purchase-list')
        response = client.get(url, content_type='application/json')
        assert response.status_code == 403

    @pytest.mark.django_db
    def test_delete_purchase_successful(self, client, django_user_model, auth_token, post_book):
        """order delete success"""
        token = auth_token
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_AUTHORIZATION=token, content_type='application/json')
        cart_id = response.data["data"]["id"]
        url = reverse('purchase-detail', args=[cart_id])
        response = client.delete(url, HTTP_AUTHORIZATION=token, content_type='application/json')
        assert response.status_code == 403

    @pytest.mark.abc
    @pytest.mark.django_db
    def test_delete_purchase_successful(self, client, django_user_model, auth_token, post_book):
        """order delete success"""
        token = auth_token
        book = post_book
        create_cart = {
            "book": book,
            "total_quantity": 3,
        }
        url = reverse('cart-list')
        response = client.post(url, create_cart, HTTP_AUTHORIZATION=token, content_type='application/json')
        cart_id = response.data["data"]["id"]
        url = reverse('purchase-detail', args=[cart_id])
        response = client.delete(url, content_type='application/json')
        assert response.status_code == 403
