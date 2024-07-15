from django.contrib.auth.views import LoginView, LogoutView
from .views import RegisterView, CustomPasswordResetView
from django.urls import path
from users import views
from django.contrib.auth import views as auth_views

app_name = 'users'

urlpatterns = [

    path('login/', LoginView.as_view(template_name='users/login.html'), name='login'),

    path('logout/', LogoutView.as_view(next_page='/users/login/'), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('email_confirm/<str:token>/', views.email_confirm, name='email_confirmed'),
    path('custom-password-reset/', CustomPasswordResetView.as_view(), name='custom_password_reset'),
]
