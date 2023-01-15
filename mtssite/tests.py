from django.test import TestCase

from .models import CustomUser, CustomUserManager
# Create your tests here.

class AuthTests(TestCase):

    def setUp(self):
        personnel_number = '005'
        email = 'evdok12@yandex.ru'
        fio = 'Ebv Gan Mo'
        password = 'z34hg1k'

        #creating user for test db
        self.user = CustomUser.objects.create_user(personnel_number, email, fio, password)

    def test_auth_with_custom_user_class_correct_data(self):
        '''Testing authentification with correct user data'''

        self.assertIs(self.client.login(username='005', password='z34hg1k'), True)
        

    def test_auth_with_custom_user_class_incorrect_data(self):
        '''Testing authentification with incorrect user data'''

        #all data is incorrect
        self.assertIs(self.client.login(username='001', password='zzzz'), False)
        #correct login
        self.assertIs(self.client.login(username='005', password='zzzzz'), False)
        #correct password
        self.assertIs(self.client.login(username='001', password='z34hg1k'), False)
        #empty data
        self.assertIs(self.client.login(username='', password=''), False)

    