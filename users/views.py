import random
import string
import secrets
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.views import View
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from django.conf import settings
from .models import User
from .forms import CustomUserCreationForm


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
def send_email(email, new_password):
    subject = 'Your new password'
    message = f'Your new password is: {new_password}'
    from_email = settings.DEFAULT_FROM_EMAIL
    send_mail(subject, message, from_email, [email])


class CustomPasswordResetView(View):
    def post(self, request):
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            new_password = self.generate_random_password()
            user.set_password(new_password)
            user.save()
            send_email(user.email, new_password)
            return JsonResponse(
                {'status': 'success', 'message': 'Password reset successfully. Check your email for the new password.'})
        except User.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'User with this email does not exist.'})

    @staticmethod
    def generate_random_password(length=8):
        characters = string.ascii_letters + string.digits + string.punctuation
        return ''.join(random.choice(characters) for _ in range(length))

    @staticmethod
    def send_email(email, new_password):
        subject = 'Your new password'
        message = f'Your new password is: {new_password}'
        from_email = settings.DEFAULT_FROM_EMAIL
        send_mail(subject, message, from_email, [email])
