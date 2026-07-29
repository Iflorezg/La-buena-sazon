from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect

from accounts.forms import AccountCreationForm, LoginForm


def home(request):
    return render(request, "home.html")


class AccountLoginView(LoginView):
    template_name = "login.html"
    authentication_form = LoginForm
    redirect_authenticated_user = True


def logout_view(request):
    logout(request)
    return redirect("home")

def profile_view(request):
    if request.method == "POST":
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "exit.html")
    else:
        form = AccountCreationForm()

    return render(request, "accounts.html", {'form': form})