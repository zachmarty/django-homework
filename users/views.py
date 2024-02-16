from django.db.models.base import Model as Model
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView
from config import settings
from users.models import User
from users.forms import UserProfileForm, UserRegisterForm
from django.core.mail import send_mail



class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.is_active = True
        new_user.save()
        send_mail(
            subject="Приветствуем на нашем сайте",
            message=f"Вы успешно зарегестрировались",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],
        )
        return super().form_valid(form)


class EmailConfirmationSentView(TemplateView):
    pass


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user
