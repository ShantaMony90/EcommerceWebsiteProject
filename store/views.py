from django.shortcuts import render, redirect
from .models import *
from .forms import *

# Create your views here.

def index(request):
    banner = Banner.objects.all()
    context = {
        'banner': banner,
    }
    return render(request, 'index.html', context)


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')
    else:
        form = ContactForm()

    return render(request, 'contact.html', {'form': form})



def dashboard_page(request):
    if request.method == 'POST':
        form_2 = DashboardForm(request.POST)
        if form_2.is_valid():
            form_2.save()
            return redirect('dashboard')
    else:
        form_2 = DashboardForm()
    return render(request, 'dashboard.html', {'form_2': form_2})


def product(request):
    return render(request, 'product.html')
