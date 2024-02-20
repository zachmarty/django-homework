from django.db.models.base import Model as Model
from django.forms import ValidationError
from django.shortcuts import redirect, render
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView
from config import settings
from users.models import User
from users.forms import UserProfileForm, UserRegisterForm
from django.core.mail import send_mail
import secrets


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.token = secrets.token_urlsafe(20)
        new_user.save()
        
        send_mail(
            subject="Приветствуем на нашем сайте",
            message=f"Вы успешно зарегестрировались, для завершения авторизации, введите данный код {new_user.token}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],
        )
        return redirect('/users/verify', kwargs={"user":new_user})   


class VerifyView(TemplateView):
    template_name = 'users/verify.html'
    success_url = reverse_lazy("users:profile")
    
    def form_valid(self, form):
        
        user = User.objects.get(verify_key=self.kwargs["user"])
        if form.data['key'] == user.verify_key:
            user.is_active = True
            user.save()    
            return super().form_valid(form)
        else:
            raise ValidationError(form.data['key'].error_message['invalid'])
    
    
    


class ProfileView(UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user
