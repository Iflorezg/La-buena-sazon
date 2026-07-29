from django.shortcuts import render, redirect

from accounts.forms import AccountCreationForm

def home(request):
    return render(request, "home.html")

def profile_view(request):
    if request.method == "POST":
        form = AccountCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, "exit.html")
    else:
        form = AccountCreationForm()

    return render(request, "accounts.html", {'form': form})