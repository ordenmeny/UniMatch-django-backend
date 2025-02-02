from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import TemplateView
from django.views.generic.edit import UpdateView

import uuid


class CustomLoginView(LoginView):
    template_name = 'users/login.html'


class GetBotView(LoginRequiredMixin, TemplateView):
    template_name = 'users/get_bot.html'

    def get_context_data(self, **kwargs):
        kwargs = super().get_context_data(**kwargs)
        kwargs['uniq_code'] = self.uniq_code

        return kwargs

    def dispatch(self, request, *args, **kwargs):
        user = request.user

        if not user.uniq_code and not user.chat_id:
            uniq_code = str(uuid.uuid4())
            self.uniq_code = uniq_code

            user.uniq_code = uniq_code
            user.save()
        else:
            self.uniq_code = user.uniq_code

        return super().dispatch(request, *args, **kwargs)
