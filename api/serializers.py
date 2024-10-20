from .models import User, Ingredient, DietPlan
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'email', 'first_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user

class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ['name', 'grams', 'protein', 'fat', 'carbs']

class DietPlanSerializer(serializers.ModelSerializer):
    ingredients = IngredientSerializer(many=True)
    
    class Meta:
        model = DietPlan
        fields = ['user', 'meals', 'total_calories', 'ingredients', 'created_at']
    
    def create(self, validated_data):
        ingredients_data = validated_data.pop('ingredients')
        diet_plan = DietPlan.objects.create(**validated_data)
        for ingredient_data in ingredients_data:
            Ingredient.objects.create(diet_plan=diet_plan, **ingredient_data)
        return diet_plan