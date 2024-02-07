from django.shortcuts import render, redirect
from az_admin.forms import LoginForm, RegistrationForm, UserPasswordResetForm, UserSetPasswordForm, \
    UserPasswordChangeForm
from django.contrib.auth import logout

from django.contrib.auth import views as auth_views


def pages_maintenence(request):
    return render(request, 'pages/pages_maintenence.html')


# Create your views here.

# Authentication
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            print('Account created successfully!')
            return redirect('/accounts/login/')
        else:
            print("Registration failed!")
    else:
        form = RegistrationForm()

    context = {'form': form}
    return render(request, 'accounts/register.html', context)


class UserLoginView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    form_class = LoginForm
    success_url = '/'


class UserPasswordResetView(auth_views.PasswordResetView):
    template_name = 'accounts/forgot-password.html'
    form_class = UserPasswordResetForm


class UserPasswordResetViewV1(auth_views.PasswordResetView):
    template_name = 'pages/examples/forgot-password.html'
    form_class = UserPasswordResetForm


class UserPasswordResetConfirmView(auth_views.PasswordResetConfirmView):
    template_name = 'accounts/recover-password.html'
    form_class = UserSetPasswordForm


class UserPasswordChangeView(auth_views.PasswordChangeView):
    template_name = 'accounts/password_change.html'
    form_class = UserPasswordChangeForm


def user_logout_view(request):
    logout(request)
    return redirect('/accounts/login/')


def index(request):
    return render(request, 'index.html')


def pages_maintenance(request):
    return render(request, 'pages/maintenance.html')
