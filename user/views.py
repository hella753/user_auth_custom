from django.contrib.auth import login
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView
from user.forms import RegistrationForm
from utils.utils import set_activity_expiry


class RegistrationView(CreateView):
    form_class = RegistrationForm
    template_name = "registration/register.html"
    success_url = reverse_lazy("store:index")

    def form_valid(self, form):
        user = form.save()
        if user:
            login(self.request, user)
            set_activity_expiry(self.request)
            return redirect(self.success_url)
        else:
            return super().form_valid(form)


class Login(LoginView):
    template_name = 'registration/login.html'

    def get_success_url(self):
        set_activity_expiry(self.request)
        return super().get_success_url()
