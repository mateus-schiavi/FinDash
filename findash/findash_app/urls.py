from django.urls import path
from findash_app import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('api/login/', views.api_login, name='api_login'),
]
