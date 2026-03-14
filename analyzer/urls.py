# analyzer/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('team/', views.team, name='team'),
    path('privacy/', views.privacy_analyzer, name='privacy'),
    
    # New Static Information Pages
    path('terms/', views.terms_service, name='terms'),
    path('privacy-policy/', views.privacy_policy, name='privacy_policy'),
    
    # API Endpoints
    path("api/find-policy/", views.find_and_analyze_app, name="find_policy"),
    path('api/analyze/', views.analyze_policy, name='analyze_policy'),
]