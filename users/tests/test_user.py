import pytest
from rest_framework.reverse import reverse


class TestUser:
    @pytest.mark.django_db
    def test_user_reg_succ(self, client, django_user_model):
        """user registration success"""
        user_data = {
            "username": "lalu123",
            "password": "lalu12345",
            "first_name": "vasu",
            "last_name": "kv",
            "email": "ksam071@gmail.com",
            "phone": 756848777,
            "location": "Delhi"

        }
        url = reverse('user_reg')
        response = client.post(url, user_data, content_type="application/json")
        assert response.status_code == 201

    @pytest.mark.django_db
    def test_user_reg_unsucc(self, client, django_user_model):
        """user registration fail"""
        user_data = {
            "username": "",
            "password": "lalu12345",
            "first_name": "vasu",
            "last_name": "kv",
            "email": "ksam071@gmail.com",
            "phone": 756848777,
            "location": "Delhi"

        }
        url = reverse('user_reg')
        response = client.post(url, user_data, content_type="application/json")
        assert response.status_code == 400

    @pytest.mark.django_db
    def test_user_login_pass(self, client, django_user_model):
        """user login success"""
        user_data = {
            "username": "lalu123",
            "password": "lalu12345",
            "first_name": "vasu",
            "last_name": "kv",
            "email": "ksam071@gmail.com",
            "phone": 756848777,
            "location": "Delhi"

        }
        url = reverse('user_reg')
        response = client.post(url, user_data, content_type="application/json")
        user = django_user_model.objects.get(id=response.data["data"]["id"])
        user.is_verified = True
        user.save()
        login_data = {
            "username": "lalu123",
            "password": "lalu12345"
        }
        login_url = reverse('user_login')
        response = client.post(login_url, login_data)
        print(response.data)

        assert response.status_code == 200

    @pytest.mark.z
    @pytest.mark.django_db
    def test_user_login_fail(self, client, django_user_model):
        """user login fail"""
        user_data = {
            "username": "lalu123",
            "password": "lalu12345",
            "first_name": "vasu",
            "last_name": "kv",
            "email": "ksam071@gmail.com",
            "phone": 756848777,
            "location": "Delhi"

        }
        url = reverse('user_reg')
        response = client.post(url, user_data, content_type="application/json")
        user = django_user_model.objects.get(id=response.data["data"]["id"])
        user.is_verified = True
        user.save()
        login_data = {
            "username": "lalu123",
            "password": ""
        }
        login_url = reverse('user_login')
        response = client.post(login_url, login_data)
        print(response.data)

        assert response.status_code == 400
