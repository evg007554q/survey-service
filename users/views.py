from django.contrib.auth.views import LoginView as BaseLoginView
from django.contrib.auth.views import LogoutView as BaseLogoutView


class LoginView(BaseLoginView):
    # pass
    template_name = 'users/login.html'


class LogoutView(BaseLogoutView):
    pass