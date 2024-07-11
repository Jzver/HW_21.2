import secrets
from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm, UserRegisterForm
from django.contrib.auth.views import PasswordResetView as AuthPasswordResetView
from users.models import User
from django.contrib.auth.forms import PasswordResetForm
from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import views as auth_views


# Класс для регистрации пользователя
class RegisterView(CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('users:login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f'http://{host}/users/email_confirm/{token}'
        send_mail(
            'Подтверждение регистрации',
            f'Спасибо за регистрацию. Пожалуйста, подтвердите ваш аккаунт, перейдя по следующей ссылке: {url}',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return super().form_valid(form)


def email_confirm(request, token):
    user = get_object_or_404(User, token=token)
    if not user.is_active:
        user.is_active = True
        user.token = ''  # Очистка токена после активации
        user.save()
        messages.success(request, 'Ваш аккаунт был активирован.')
        return redirect('users:login')  # Перенаправление на страницу входа
    else:
        messages.info(request, 'Аккаунт уже был активирован.')
        return redirect('users:login')


# Класс для сброса пароля
class PasswordResetView(AuthPasswordResetView):
    template_name = 'users/password_reset_form.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_email.txt'
    success_url = reverse_lazy('users/password_reset_done')

    def post(self, request, *args, **kwargs):
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            opts = {
                'use_https': request.is_secure(),
                'token_generator': default_token_generator,
                'from_email': settings.DEFAULT_FROM_EMAIL,
                'email_template_name': self.email_template_name,
                'subject_template_name': self.subject_template_name,
                'request': request,
            }
            form.save(**opts)
            return super(PasswordResetView, self).form_valid(form)
        else:
            return self.form_invalid(form)


class PasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'password_reset_confirm.html'
    success_url = reverse_lazy('users:login')


class PasswordResetDoneView(auth_views.PasswordResetDoneView):
    template_name = 'password_reset_done.html'


class PasswordResetCompleteView(auth_views.PasswordResetCompleteView):
    template_name = 'password_reset_complete.html'
    success_url = reverse_lazy('users:login')
