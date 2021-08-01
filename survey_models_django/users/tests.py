from django.test import TestCase
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

from django.test import Client


class AuthUserTests(TestCase):
    
    username = "Steve"
    password = "testpassword123"

    def setUp(self) -> None:
        self.user = get_user_model().objects.create_user(username='test',
                                                         password='12test12')
        self.client = Client()

    def tearDown(self):
        self.user.delete()

    def test_std_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(
            username='testname',
            password='testpassword'
        )
        self.assertEqual(user.username, 'testname')
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_custom_create_user(self):
        test_name = "Ivan"
        resp = self.client.post('/auth/register/', data={"username": test_name,
                                               "password1": self.password,
                                               "password2": self.password})
        user = User.objects.get(username=test_name)
        self.assertEqual(user.username, test_name)
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
    
    def test_register_user_page(self):
        resp = self.client.get('/auth/register/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/register.html')
    
    def test_login_user_page(self):
        resp = self.client.get('/auth/login/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'users/login.html')
    
    def test_login_correct(self):
        response = self.client.post('/auth/login/', {'username': 'test', 'password': '12test12'})
        self.assertTrue(response.status_code, 302)
    
    def test_logout(self):
        self.client.post('/auth/login/', {'username': 'test', 'password': '12test12'})
        resp = self.client.get('/auth/logout/')
        self.assertEqual(resp.status_code, 302)
    
