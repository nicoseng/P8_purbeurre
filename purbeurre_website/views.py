import random

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CreateUser, ProductForm
from .product_extractor import ProductExtractor
from .substitute_extractor import SubstituteExtractor


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

    if request.method == "POST":
        context = {}
        product_name = request.POST.get('product_name')
        context["product_name"] = product_name
        # product_data = ProductExtractor()
        # get_products_url = product_data.extract_products_url(product_name)
        # get_products_data = product_data.extract_products(get_products_url)
        return render(request, 'purbeurre_website/check_my_products.html', context)


def display_results(request):
    if request.method == "POST":
        product_name = request.POST.get('product_name')
        product_data = ProductExtractor()
        get_products_url = product_data.extract_products_url(product_name)
        get_products_data = product_data.extract_products(get_products_url)
        print(get_products_data)
        context = {"product_name": product_name, "products": get_products_data, "product_image": get_products_data[len(get_products_data)-1]["product_image"]}
        return render(request, 'purbeurre_website/display_results.html', context)

    else:
        messages.info(request, "Le nom du produit est introuvable.")
        return render(request, 'purbeurre_website/display_results.html', messages)



def display_substitute(request):

    if request.method == "GET":
        product_data = request.GET.get('substitute')

        test = SubstituteExtractor()
        get_products_data = test.get_substitute(product_data)
        print(get_products_data)
        context = {"products": get_products_data}
        return render(request, 'purbeurre_website/display_substitute.html',context)

    else:
        messages.info(request, "Le nom du produit est introuvable.")
        return render(request, 'purbeurre_website/display_results.html', messages)


def add_product(request):
    return render(request, 'purbeurre_website/display_results.html')


def delete_product(request):
    return render(request, 'purbeurre_website/display_results.html')


