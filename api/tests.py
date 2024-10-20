from django.test import TestCase
from django.urls import reverse
from unittest.mock import patch, MagicMock
from rest_framework import status
from .models import User, DietPlan, Ingredient
from rest_framework.exceptions import AuthenticationFailed  
from django.test import TestCase
from django.urls import reverse
from rest_framework import status


class UserAPITests(TestCase):

    @patch('api.views.RefreshToken') 
    def test_login_user(self, mock_refresh_token):
        user = User.objects.create_user(username='testuser', password='testpass')
        mock_refresh_token.for_user.return_value = mock_refresh_token
        
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass',
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        self.assertIn('refresh', response.data)
    
    @patch('api.views.UserSerializer') 
    def test_register_user(self, mock_user_serializer):
        mock_user_serializer.return_value.is_valid.return_value = True
        mock_user_serializer.return_value.save.return_value = None
        
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password': 'newpass',
            'email': 'newuser@example.com'
        })
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['msg'], "User registered successfully.")
    
    @patch('api.views.authenticate')
    def test_login_user_invalid(self, mock_authenticate):
        mock_authenticate.return_value = None
        
        response = self.client.post(reverse('login'), {
            'username': 'invaliduser',
            'password': 'wrongpass',
        })
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    @patch('api.views.JWTAuthentication')
    def test_validate_token_invalid(self, mock_jwt_authentication):
        mock_instance = mock_jwt_authentication.return_value
        mock_instance.authenticate.side_effect = AuthenticationFailed("Token is invalid.")

        response = self.client.post(reverse('validate_token'), {
            'token': 'invalidtoken'
        })

        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.data['msg'], "Token is invalid.")

    @patch('api.views.RefreshToken')
    def test_refresh_token(self, mock_refresh_token):
        mock_refresh_token.return_value.access_token = 'new_access_token'
        
        response = self.client.post(reverse('refresh_token'), {
            'refresh': 'valid_refresh_token'
        })
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['access'], 'new_access_token')

    @patch('api.views.JWTAuthentication')
    def test_save_diet_no_data(self, mock_jwt_authentication):
        user = User.objects.create_user(username='testuser', password='testpass')
        mock_instance = mock_jwt_authentication.return_value
        mock_instance.authenticate.return_value = (user, None)

        response = self.client.post(reverse('save_diet', args=['testuser']), {})

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], 'No data provided')

    @patch('api.views.JWTAuthentication')
    def test_save_diet_user_not_found(self, mock_jwt_authentication):
        user = User.objects.create_user(username='testuser', password='testpass')
        mock_instance = mock_jwt_authentication.return_value
        mock_instance.authenticate.return_value = (user, None)

        response = self.client.post(reverse('save_diet', args=['invaliduser']), {
            'ingredients': {
                'Chicken': {'grams': 200, 'protein': 30, 'fat': 10, 'carbs': 0},
            },
            'totalCalories': 500
        })

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'User not found')

    @patch('api.views.JWTAuthentication')
    def test_show_diets_success(self, mock_jwt_authentication):
        user = User.objects.create_user(username='testuser', password='testpass')
        diet_plan = DietPlan.objects.create(user=user, total_calories=500)
        ingredient = Ingredient.objects.create(name='Chicken', grams=200, protein=30, fat=10, carbs=0)
        diet_plan.ingredients.add(ingredient)  # Use the add method

        mock_instance = mock_jwt_authentication.return_value
        mock_instance.authenticate.return_value = (user, None)

        response = self.client.get(reverse('show_diets', args=['testuser']))

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('ingredients', response.data)

    @patch('api.views.JWTAuthentication')
    def test_show_diets_no_diet_plan(self, mock_jwt_authentication):
        user = User.objects.create_user(username='testuser', password='testpass')
        mock_instance = mock_jwt_authentication.return_value
        mock_instance.authenticate.return_value = (user, None)

        response = self.client.get(reverse('show_diets', args=['testuser']))

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['error'], 'No diet plan found for this user')