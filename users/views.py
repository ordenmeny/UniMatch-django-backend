from django.contrib.auth import get_user_model, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView, CreateView
import uuid
from .forms import *




class CustomLoginView(LoginView):
    template_name = 'users/login.html'
    success_url = reverse_lazy('users:get_bot')

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['uniq_code'] = str(uuid.uuid4())

        # Сохраняем uniq_code в сессии браузера.
        self.request.session['uniq_code'] = uniq_code

        # print(self.request.session['uniq_code']) # из сессии браузера.

        return kwargs

    def get_success_url(self):
        return self.success_url


class GetBotView(LoginRequiredMixin, TemplateView):
    template_name = 'users/get_bot.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['uniq_code'] = self.uniq_code

        return kwargs

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not request.user.is_authenticated:
            return redirect('admin:login')

        # Если у пользователя нет uniq_code или нет chat_id:
        # у пользователя генерируем uniq_code
        # и передаем в контекст для создания ссылки на тг-бот.
        # Если есть uniq_code, но нет chat_id,
        # то передаем в контекст uniq_code.
        if not user.uniq_code and not user.chat_id:
            uniq_code = str(uuid.uuid4())
            self.uniq_code = uniq_code

            user.uniq_code = uniq_code
            user.save()
        else:
            self.uniq_code = user.uniq_code

        return super().dispatch(request, *args, **kwargs)


class SignUpView(CreateView):
    model = get_user_model()
    form_class = CustomUserCreationForm
    template_name = "users/signup.html"
    success_url = reverse_lazy('users:get_bot')

    def form_valid(self, form):
        # Создаем объект пользователя, но пока не сохраняем в БД
        user = form.save(commit=False)

        # Генерируем и присваиваем уникальный код
        uniq_code = str(uuid.uuid4())
        user.uniq_code = uniq_code
        # self.uniq_code = uniq_code

        # Сохраняем пользователя в БД
        user.save()

        # Аутентифицируем пользователя
        authenticated_user = authenticate(username=user.username, password=self.request.POST['password1'])

        if authenticated_user:
            login(self.request, authenticated_user)

        # return redirect(f"https://t.me/Uni_Match_Bot?start={uniq_code}")
        return redirect(reverse_lazy('users:get_bot'))