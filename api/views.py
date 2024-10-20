from django.http import JsonResponse
from django.contrib.auth import authenticate
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer, DietPlanSerializer, IngredientSerializer
from .models import User, DietPlan, Ingredient


def check_status(request):
    return JsonResponse({'status': 200})

@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        _ = serializer.save()
        return Response({"msg": "User registered successfully."}, status=status.HTTP_201_CREATED)
    return Response({"msg": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)

    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
            'email': str(user.email),
            'username': str(user.username),
            'name': str(user.first_name),
        })
    return Response({"msg": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def refresh_token(request):
    refresh_token = request.data.get('refresh')
    if refresh_token is None:
        return Response({"msg": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        refresh = RefreshToken(refresh_token)
        new_access_token = str(refresh.access_token)

        return Response({
            'access': new_access_token,
        }, status=status.HTTP_200_OK)
    except Exception as e:
        return Response({"msg": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
def validate_token(request):
    try:
        JWT_authenticator = JWTAuthentication()
        JWT_authenticator.authenticate(request)
        return Response({"msg": "Token is valid."}, status=status.HTTP_200_OK)
    except Exception:
        return Response({"msg": "Token is invalid."}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def save_diet(request, username):
    try:
        JWT_authenticator = JWTAuthentication()
        JWT_authenticator.authenticate(request)

        data = request.data
        if not data:
            return Response({'error': 'No data provided'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)

        ingredients_dict = data.get('ingredients', {})
        ingredients_list = [
            {
                'name': name,
                'grams': float(details['grams']),
                'protein': float(details['protein']),
                'fat': float(details['fat']),
                'carbs': float(details['carbs'])
            } for name, details in ingredients_dict.items()
        ]

        total_calories = data.get('totalCalories', 2000)
        if total_calories is None:
            return Response({'error': 'totalCalories is required'}, status=status.HTTP_400_BAD_REQUEST)

        data['total_calories'] = float(total_calories)
        data['user'] = user.id
        data['ingredients'] = ingredients_list

        serializer = DietPlanSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    except Exception:
        return Response({"msg": "Token is invalid."}, status=status.HTTP_401_UNAUTHORIZED)
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET'])
def show_diets(request, username):
    try:
        JWT_authenticator = JWTAuthentication()
        JWT_authenticator.authenticate(request)
    
        user = get_object_or_404(User, username=username)

        diet_plan = DietPlan.objects.filter(user=user).order_by('-created_at').first()

        if not diet_plan:
            return Response({'error': 'No diet plan found for this user'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = DietPlanSerializer(diet_plan)
        return Response(serializer.data, status=status.HTTP_200_OK)
    except Exception:
        return Response({"msg": "Token is invalid."}, status=status.HTTP_401_UNAUTHORIZED)