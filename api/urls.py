from django.urls import path
from api import views


urlpatterns = [
    path("status/", views.check_status, name="status"),
    path('register/', views.register, name='register'),
    path('refresh-token/', views.refresh_token, name='refresh_token'),
    path('validate-token/', views.validate_token, name='validate_token'),
    path('login/', views.login, name='login'),
    path('save-diet/<str:username>/', views.save_diet, name='save_diet'),
    path('show-diets/<str:username>/', views.show_diets, name='show_diets'),
]