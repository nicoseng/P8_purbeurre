import ast

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from requests import exceptions, get
from urllib3.util import retry

from .category_injector_in_table import CategoryInjectorInTable
from .category_loader import CategoriesLoader
from .forms import CreateUser
from .models import Substitute, Basket, Product, Category
from .product_extractor import ProductExtractor
from .category_extractor import CategoriesExtractor
from .product_injector_in_table import ProductInjectorInTable
from .substitute_extractor import SubstituteExtractor
from .substitute_injector_in_table import SubstituteInjectorInTable


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


def add_product(request):
    if request.method == "POST":
        substitute_selected_data = request.POST.get('substitute_selected_data')
        substitute_selected_data = ast.literal_eval(substitute_selected_data)

        print(substitute_selected_data)
        print(type(substitute_selected_data))

        context = {"substitute_selected_data": substitute_selected_data}

        return render(request, 'purbeurre_website/add_product.html', context)


def check_my_account(request):
    return render(request, 'purbeurre_website/check_my_account.html')


def check_my_basket(request):
    if request.method == "POST":
        substitute_selected_data = request.POST.get('substitute_selected_data')
        substitute_selected_data = ast.literal_eval(substitute_selected_data)
        print(substitute_selected_data)
        substitute_name = substitute_selected_data["product_name"]
        substitute_nutriscore = substitute_selected_data["nutriscore"]
        substitute_image = substitute_selected_data["product_image"]
        substitute_url = substitute_selected_data["url"]

        substitute_selected_data_table = Basket.objects.all()

        substitute_selected_data = Basket(
            substitute_name=substitute_name,
            substitute_nutriscore=substitute_nutriscore,
            substitute_image=substitute_image,
            substitute_url=substitute_url
        )
        for row in substitute_selected_data_table:
            if substitute_selected_data.substitute_url == row.substitute_url:
                pass

            else:
                substitute_selected_data.save()

        table_displayed = Substitute.objects.all()
        context = {"table_displayed": table_displayed}

    return render(request, 'purbeurre_website/check_my_basket.html', context)


def check_product(request):
    if request.method == "POST":
        product_selected_data = request.POST.get('product_selected_data')
        product_selected_data = ast.literal_eval(product_selected_data)

        context = {"product_selected_data": product_selected_data}
        return render(request, 'purbeurre_website/check_product.html', context)


def check_substitute(request):
    if request.method == "POST":
        substitute_selected = request.POST.get('substitute_selected')
        substitute_selected_data = request.POST.get('substitute_selected_data')
        return render(request, 'purbeurre_website/check_substitute.html')

        # context = {
        #     "product_name": substitute_selected,
        #     "substitute_selected_data": substitute_selected_data
        # }
        # return render(request, 'purbeurre_website/check_substitute.html', context)


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


def display_results(request):
    if request.method == "POST":
        searched_product_name = request.POST.get('searched_product_name')
        searched_product_data = ProductExtractor()
        searched_products_url = searched_product_data.extract_products_url(searched_product_name)

        products_list = searched_product_data.extract_products(searched_products_url)

        if len(products_list) == 0:
            messages.info(request, "Il n'y a pas de produit correspondant à votre recherche.")
            return redirect('home')

        else:
            category_list = CategoriesLoader()
            category_list = category_list.load_categories()

            category_table = CategoryInjectorInTable()
            category_table = category_table.inject_category_in_table(category_list)

            product_table = ProductInjectorInTable()
            product_table = product_table.inject_product_in_table(products_list, category_table)

            context = {"product_name": searched_product_name,
                       "products": product_table
                       }
            return render(request, 'purbeurre_website/display_results.html', context)


def display_substitute(request):
    if request.method == "POST":
        product_selected = request.POST.get('product_selected')
        print(product_selected)
        product_selected_data = request.POST.get('product_selected_data')
        # product_selected_data = ast.literal_eval(product_selected_data)

        product_selected_id = request.POST.get('product_selected_id')

        # Récupérer la catégorie du produit sélectionné
        # product_selected_category = product_selected_data["categories"]
        #product_selected_category = product_selected_category.split(",")

        category_extracted = CategoriesExtractor()
        categories_list_url = category_extracted.extract_categories_url(product_selected_category)

        products_list = ProductExtractor()
        products_list = products_list.extract_products(categories_list_url)

        substitute_proposed_list = SubstituteExtractor()
        substitute_proposed_list = substitute_proposed_list.get_substitute(products_list, product_selected_data)

        substitute_table = SubstituteInjectorInTable()
        substitute_table = substitute_table.inject_substitute_in_table(substitute_proposed_list,)

        context = {
            "product_selected": product_selected,
            "product_selected_data": product_selected_data,
            "substitute_proposed_list": substitute_proposed_list,
            "substitute_table": substitute_table
        }

        return render(request, 'purbeurre_website/display_substitute.html', context)
    #
    # else:
    #     messages.info(request, "Il n'y a pas de substitut disponible.")
    #     return render(request, 'purbeurre_website/display_results.html', messages)


@login_required(login_url='login')
def home(request):
    return render(request, 'purbeurre_website/home.html')


def logout_user(request):
    logout(request)
    return redirect('login')


def delete_product(request):
    return render(request, 'purbeurre_website/display_results.html')
