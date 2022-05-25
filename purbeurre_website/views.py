import ast

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .forms import CreateUser, ProductForm
from .product_extractor import ProductExtractor
from .category_extractor import CategoriesExtractor
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
        product_selected_data = request.POST.get('product_selected_data')
        print(product_selected_data)
        product_selected_data = ast.literal_eval(product_selected_data)
        print(product_selected_data)

        print(product_selected_data["product_name"])
        context = {"product_selected_data": product_selected_data}
        return render(request, 'purbeurre_website/check_my_products.html', context)


def display_results(request):
    if request.method == "POST":
        searched_product_name = request.POST.get('searched_product_name')
        searched_product_data = ProductExtractor()
        searched_products_url = searched_product_data.extract_products_url(searched_product_name)
        products_data = searched_product_data.extract_products(searched_products_url)
        context = {"product_name": searched_product_name, "products": products_data}
        return render(request, 'purbeurre_website/display_results.html', context)

    else:
        messages.info(request, "Le nom du produit est introuvable.")
        return render(request, 'purbeurre_website/display_results.html', messages)


def display_substitute(request):

    if request.method == "POST":
        product_selected = request.POST.get('product_selected')
        product_selected_data = request.POST.get('product_selected_data')
        product_selected_data = ast.literal_eval(product_selected_data)
        product_selected_category = product_selected_data["categories"]
        #print(product_selected_category)
        #print(type(product_selected_category))
        product_selected_category = product_selected_category.split(",")
        #print(product_selected_category)
        #print(type(product_selected_category))
        category_extracted = CategoriesExtractor()
        categories_list_url = category_extracted.extract_categories_url(product_selected_category)
        #print(categories_list_url)
        products_list = ProductExtractor()
        products_list = products_list.extract_products(categories_list_url)
        print(products_list)
        substitute_proposed_list = SubstituteExtractor()
        substitute_proposed_list = substitute_proposed_list.get_substitute(products_list, product_selected_data)
        #print(substitute_proposed_list)

        context = {
            "product_selected": product_selected,
            "product_selected_data": product_selected_data,
            "substitute_proposed_list": substitute_proposed_list}
        return render(request, 'purbeurre_website/display_substitute.html', context)

    else:
        messages.info(request, "Le nom du produit est introuvable.")
        return render(request, 'purbeurre_website/display_results.html', messages)


def add_product(request):
    if request.method == "POST":
        context = {}
        product_name = request.POST.get('sauvegarder')
        context["product_name"] = product_name
        # product_data = ProductExtractor()
        # get_products_url = product_data.extract_products_url(product_name)
        # get_products_data = product_data.extract_products(get_products_url)
        return render(request, 'purbeurre_website/add_product.html', context)
    return render(request, 'purbeurre_website/add_product.html')


def delete_product(request):
    return render(request, 'purbeurre_website/display_results.html')


