from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import SignupForm


def signup_view(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard_home')
    else:
        form = SignupForm()

    return render(request, 'accounts/signup.html', {'form': form})
