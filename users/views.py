from django.db.models.base import Model as Model
from django.forms import ValidationError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, TemplateView
from config import settings
from users.models import User
from users.forms import UserProfileForm, UserRegisterForm
from django.core.mail import send_mail
import secrets
from django.contrib.auth.mixins import LoginRequiredMixin


class RegisterView(CreateView):
    model = User
    form_class = UserRegisterForm
    template_name = "users/register.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        new_user = form.save(commit=False)
        new_user.is_active = False
        new_user.verify_key = secrets.token_urlsafe(20)
        new_user.save()

        send_mail(
            subject="Приветствуем на нашем сайте",
            message=f"Вы успешно зарегестрировались, для завершения авторизации, введите данный код {new_user.verify_key}",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[new_user.email],
        )
        return redirect("/users/verify", kwargs={"user": new_user})


class VerifyView(TemplateView):
    template_name = "users/verify.html"
    success_url = reverse_lazy("users:profile")
    http_method_names = ["post", "get"]
            

    def post(self, request, *args, **kwargs):
        key = request.POST["key"]
        try:
            user = User.objects.get(verify_key = key)
            user.is_active = True
            user.save()
            return HttpResponseRedirect(reverse_lazy("users:login"))
        except:
            data = {"error":"Ключ не верный"}
            return render(request, "users/verify.html", data)



class ProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


def generate_new_password(request):
    new_pass = secrets.token_urlsafe(20)
    request.user.set_password(new_pass)
    request.user.save()
    send_mail(
            subject="Уведомление о смене пароля",
            message=f"Новый пароль был успешно сгенерирован: {new_pass}. Пожалуйста не забудьте его.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[request.user.email],
        )
    return redirect(reverse("users:login"))