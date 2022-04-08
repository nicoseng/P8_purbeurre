from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from purbeurre_website.category_loader import CategoryExtractor
from .forms import CreateUser


# Create your views here.
@login_required(login_url='login')
def home(request):
    return render(request, 'purbeurre_website/home.html')


def create_account(request):
    create_account_form = CreateUser()
    if request.method == "POST":
        create_account_form = CreateUser(request.POST)
        if create_account_form.is_valid():
            create_account_form.save()
            user = create_account_form.cleaned_data.get('username')
            messages.success(request, 'Compte crée avec succès pour ' + user + ' !')
            return redirect('login')

    form = {'create_account_form': create_account_form}
    return render(request, 'purbeurre_website/create_account.html', form)


def access_login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Bienvenue sur le site de Pur Beurre ' + user.username + ' !')
            return redirect('home')
        else:
            messages.info(request, "Utilisateur et/ou mot de passe inconnus")
    return render(request, 'purbeurre_website/access_login.html')


def check_my_account(request):
    return render(request, 'purbeurre_website/check_my_account.html')


def logout_user(request):
    logout(request)
    return redirect('login')


def check_my_products(request):
    return render(request, 'purbeurre_website/check_my_products.html')


def display_results(request):
    return render(request, 'purbeurre_website/display_results.html')


def get_categories(request):
    data = CategoryExtractor()
    get_data = data.load_categories()
    context = {"data": get_data}
    return render(request,'purbeurre_website/categories.html',context )
