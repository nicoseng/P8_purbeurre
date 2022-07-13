import ast

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .delete_product_in_basket import ProductEraserInBasket
from .product_injector_in_basket import ProductInjectorInBasket
from .category_injector_in_table import CategoryInjectorInTable
from .category_loader import CategoriesLoader
from .forms import CreateUser
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


def check_my_account(request):
    return render(request, 'purbeurre_website/check_my_account.html')


def display_my_basket(request):

    if request.method == "POST":
        substitute_selected_data = request.POST.get('substitute_selected_data')
        substitute_selected_data = ast.literal_eval(substitute_selected_data)

        basket_list = ProductInjectorInBasket()
        basket_list = basket_list.inject_substitute_in_basket(substitute_selected_data)

        basket_list_from_table = ProductInjectorInBasket()
        basket_list_from_table = basket_list_from_table.retrieve_substitute_from_basket(basket_list)

        print(basket_list_from_table)

        context = {"basket_list_from_table": basket_list_from_table}
        return render(request, 'purbeurre_website/display_my_basket.html', context)


def check_product(request):
    if request.method == "POST":
        product_selected_name = request.POST.get('product_selected_name')
        product_selected_data = request.POST.get('product_selected_data')
        product_selected_data = ast.literal_eval(product_selected_data)

        context = {
            "product_selected_data": product_selected_data,
            "product_selected_name": product_selected_name,
        }
        return render(request, 'purbeurre_website/check_product.html', context)


def check_substitute(request):
    if request.method == "POST":
        substitute_selected = request.POST.get('substitute_selected')
        substitute_selected_data = request.POST.get('substitute_selected_data')
        substitute_selected_data = ast.literal_eval(substitute_selected_data)

        context = {
            "product_name": substitute_selected,
            "substitute_selected_data": substitute_selected_data
        }
        return render(request, 'purbeurre_website/check_substitute.html', context)


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
        searched_products_url = searched_product_data.get_products_url(searched_product_name)
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

            product_list_from_table = ProductInjectorInTable()
            product_list_from_table = product_list_from_table.retrieve_product_from_table(product_table)

            context = {
                "product_name": searched_product_name,
                "product_list_from_table": product_list_from_table
            }

            return render(request, 'purbeurre_website/display_results.html', context)


def display_substitute(request):
    if request.method == "POST":
        product_selected_name = request.POST.get('product_selected_name')
        product_selected_data = request.POST.get('product_selected_data')
        product_selected_data = ast.literal_eval(product_selected_data)

        # We fetch the categories of the product
        category_extracted = CategoriesExtractor()
        categories_url = category_extracted.extract_categories_url(product_selected_data["category_name"])

        # We fetch the products from the relevant categories
        products_list = ProductExtractor()
        products_list = products_list.extract_products(categories_url)

        # From the products list extracted above, we choose adapted substitutes
        substitute_proposed_list = SubstituteExtractor()
        substitute_proposed_list = substitute_proposed_list.get_substitute(products_list, product_selected_data)
        print(substitute_proposed_list)

        category_list = CategoriesLoader()
        category_list = category_list.load_categories()

        category_table = CategoryInjectorInTable()
        category_table = category_table.inject_category_in_table(category_list)

        substitute_table = SubstituteInjectorInTable()
        substitute_table = substitute_table.inject_substitute_in_table(substitute_proposed_list, category_table)
        print(substitute_table)

        substitute_list_from_table = SubstituteInjectorInTable()
        substitute_list_from_table = substitute_list_from_table.retrieve_substitute_from_table(substitute_table)
        print(substitute_list_from_table)

        context = {
            "product_selected_data": product_selected_data,
            "product_selected_name": product_selected_name,
            "substitute_list_from_table": substitute_list_from_table
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

    if request.method == "POST":
        substitute_selected_data = request.POST.get('substitute_selected_data')
        substitute_selected_data = ast.literal_eval(substitute_selected_data)

        basket_list = ProductEraserInBasket()
        basket_list = basket_list.delete_substitute_in_basket(substitute_selected_data)

        basket_list_from_table = ProductInjectorInBasket()
        basket_list_from_table = basket_list_from_table.retrieve_substitute_from_basket(basket_list)

        print(basket_list_from_table)
        # messages.info(request, "Il n'y a pas de produit correspondant à votre recherche.")
    # return redirect('display_my_basket')
    return render(request, 'purbeurre_website/display_my_basket.html')
