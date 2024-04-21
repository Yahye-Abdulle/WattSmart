from django.test import TestCase, Client
from django.urls import reverse

class LoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.login_data = {
            "username":"jonthedon@gmail.com",
            "password":"JonTheDon123"
        }

    def login_view_loading(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
    
    def login_view_authentication(self):
        response = self.client.post(reverse('login'), data=self.login_data)
        self.assertEqual(response.status_code, 200)

    def login_view_wrong_information(self):
        wrong_info = {
            'username': 'testuser',
            'password': 'invalidpassword'
        }
        response = self.client.post(reverse('login'), data=wrong_info)
        self.assertEqual(response.status_code, 200)
        
    def test_logout(self):
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 200) 