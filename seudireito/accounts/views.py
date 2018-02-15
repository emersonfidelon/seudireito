from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.core.urlresolvers import reverse_lazy
from django.core.cache import cache

from .models import User
from .forms import UserAdminCreationForm, RegisterForm

def register(request):
    cache.clear()
    template_name = 'accounts/register.html'
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            user = authenticate(
                email=user.email, password=form.cleaned_data['password1']
            )
            login(request, user)
            return redirect('core:index')
    else:
        form = RegisterForm()
        
    context = {
        'form': form
    }
    return render(request, template_name, context)