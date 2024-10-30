from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views


app_name="user"
urlpatterns = [
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('register/', views.RegistrationView.as_view(), name='register'),
]
