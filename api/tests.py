from django.test import TestCase, Client
from django.urls import reverse
from .models import User

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
        
class SignupViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.signup_data = {
            "first_name":"Adam",
            "last_name":"Jones",
            "email":"adamj@gmail.com",
            "password":"AdamJones123",
            "dob":"01/05/2000"
        }
        
    def signup_view_loading(self):
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
    
    def signup_view_authentication(self):
        response = self.client.post(reverse('signup'), data=self.signup_data)
        self.assertEqual(response.status_code, 200)
        
    def signup_view_wrong_information(self):
        wrong_info = {
            "first_name":"Adam",
            "last_name":"Jones",
            "email":"adamj", # Email in wrong format
            "password":"AdamJ", # Password not meeting requirements
            "dob":"01/05/2000"
        }
        response = self.client.post(reverse('signup'), data=wrong_info)
        self.assertEqual(response.status_code, 200)
        
        self.assertTrue(User.objects.filter(email=self.signup_data['email']).exists())