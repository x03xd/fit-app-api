import pytest
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import DietPlan

User = get_user_model()

@pytest.fixture
def create_user(db):
    user = User.objects.create_user(username='testuser', password='testpassword', email='test@example.com')
    return user

@pytest.fixture
def api_client():
    from rest_framework.test import APIClient
    return APIClient()

@pytest.mark.django_db
def test_register(api_client):
    response = api_client.post(reverse('register'), {
        'username': 'testuser2',
        'password': 'testpassword',
        'email': 'test2@example.com',
        'first_name': 'Test' 
    })
    
    assert response.status_code == status.HTTP_201_CREATED
    assert response.data['msg'] == "User registered successfully."

@pytest.mark.django_db
def test_login(api_client, create_user):
    response = api_client.post(reverse('login'), {
        'username': 'testuser',
        'password': 'testpassword',
    })
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data

@pytest.mark.django_db
def test_refresh_token(api_client, create_user):
    refresh = RefreshToken.for_user(create_user)
    response = api_client.post(reverse('refresh_token'), {
        'refresh': str(refresh),
    })
    assert response.status_code == status.HTTP_200_OK
    assert 'access' in response.data

@pytest.mark.django_db
def test_validate_token(api_client, create_user):
    refresh = RefreshToken.for_user(create_user)
    access_token = str(refresh.access_token)
    
    response = api_client.post(reverse('validate_token'), HTTP_AUTHORIZATION=f'Bearer {access_token}')
    assert response.status_code == status.HTTP_200_OK
    assert response.data['msg'] == "Token is valid."

@pytest.mark.django_db
def test_validate_token_invalid(api_client):
    response = api_client.post(reverse('validate_token'), HTTP_AUTHORIZATION='Bearer invalid_token')
    assert response.status_code == status.HTTP_401_UNAUTHORIZED

@pytest.mark.django_db
def test_save_diet(api_client, create_user):
    api_client.login(username='testuser', password='testpassword')
    
    request_data = {
        'meals': {
            "avocado": {},
        },
        'totalCalories': 2000,
        'ingredients': {
            'Chicken': {'grams': 200, 'protein': 50, 'fat': 10, 'carbs': 0},
            'Rice': {'grams': 100, 'protein': 5, 'fat': 1, 'carbs': 20},
        }
    }

    response = api_client.post(reverse('save_diet', args=['testuser']), request_data, format='json')

    assert 'total_calories' in response.data
    assert response.data['total_calories'] == float(request_data['totalCalories'])
    assert len(response.data['ingredients']) == len(request_data['ingredients'])

@pytest.mark.django_db
def test_save_diet_no_data(api_client, create_user):
    api_client.login(username='testuser', password='testpassword')
    response = api_client.post(reverse('save_diet', args=['testuser']), {})
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert response.data['error'] == 'No data provided'

@pytest.mark.django_db
def test_show_diets(api_client, create_user):
    api_client.login(username='testuser', password='testpassword')
    
    api_client.post(reverse('save_diet', args=['testuser']), {
        'meals': {
            "avocado": {},
        },
        'totalCalories': 2000,
        'ingredients': {
            'Chicken': {'grams': 200, 'protein': 50, 'fat': 10, 'carbs': 0},
            'Rice': {'grams': 100, 'protein': 5, 'fat': 1, 'carbs': 20},
        }
    }, format='json')
    
    response = api_client.get(reverse('show_diets', args=['testuser']))
    assert response.status_code == status.HTTP_200_OK

@pytest.mark.django_db
def test_show_diets_not_found(api_client, create_user):
    api_client.login(username='testuser', password='testpassword')
    
    response = api_client.get(reverse('show_diets', args=['testuser']))
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.data['error'] == 'No diet plan found for this user'
