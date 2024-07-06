from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView
from .views import RegisterView
from django.urls import path

app_name = 'users'

urlpatterns = [

    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),

    path('logout/', LogoutView.as_view(next_page='/users/login/'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password_reset/', PasswordResetView.as_view(), name='password_reset'),
]
