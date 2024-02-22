"""
test for models
"""

from django.test import TestCase
from django.contrib.auth import get_user_model

class modeltest(TestCase):
    """test models"""
    def test_create_user_with_email_success(self):
        """ test creating a user an email is successful"""
        email='test@example.com'
        password='testpass123'
        user=get_user_model().objects.create_user(
            email=email,
            password=password,
        )

        self.assertEqual(user.email,email)
        self.assertTrue(user.check_password(password))

    def test_new_user_email_normal(self):
        """test email is normalized for new users"""
        sample_emails=[
            ['test1@EXAMPLE.com', 'test1@example.com'],
            ['Test2@Example.com', 'Test2@example.com'],
            ['TEST3@EXAMPLE.com', 'TEST3@example.com'],
            ['test4@example.COM', 'test4@example.com'],
        ]
        for email,expected in sample_emails:
            user=get_user_model().objects.create_user(email,'sample123')
            self.assertEqual(user.email,expected)

    def test_new_user_without_email_raise_error(self):
        """test creating user without email raises error"""
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user(None,'sample123')

    def test_create_superuser(self):
        """test creating superuser"""
        user=get_user_model().objects.create_superuser(
            'test@example.com',
            'test123'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)