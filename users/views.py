from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import UserCreationForm
from django.core.mail import send_mail
from django.conf import settings
import random
import string
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.views import View


class RegisterView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'users/register.html'

    def form_valid(self, form):
        # Сначала создаем пользователя
        user = form.save()
        # Затем отправляем письмо с подтверждением
        send_mail(
            'Подтверждение регистрации',
            'Спасибо за регистрацию, пожалуйста, подтвердите ваш аккаунт.',
            settings.DEFAULT_FROM_EMAIL,
            [user.email],
            fail_silently=False,
        )
        return super(RegisterView, self).form_valid(form)


class PasswordResetView(View):
    def post(self, request, *args, **kwargs):
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            # Генерация нового пароля
            new_password = ''.join(random.choices(string.ascii_letters + string.digits, k=8))
            user.password = make_password(new_password)
            user.save()

            # Отправка нового пароля на электронную почту пользователя
            send_mail(
                'Ваш новый пароль',
                f'Ваш новый пароль: {new_password}',
                settings.DEFAULT_FROM_EMAIL,
                [email],
                fail_silently=False,
            )
            return HttpResponse('Новый пароль был отправлен на вашу электронную почту.')
        else:
            return HttpResponse('Пользователь с таким адресом электронной почты не найден.', status=404)