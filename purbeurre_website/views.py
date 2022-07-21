import ast

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from .product_importer import ProductImporter
from .category_importer import CategoryImporter
from .forms import CreateUser
from .substitute_in_favourite import SubstituteInFavourite
from .delete_product import ProductEliminator


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


def display_user_account(request):
    return render(request, 'purbeurre_website/display_user_account.html')


def display_favourite(request):
    if request.method == "POST":

        substitute_selected_data = request.POST.get('substitute_selected_data')
        substitute_selected_data = ast.literal_eval(substitute_selected_data)

        favourite_imported = SubstituteInFavourite()
        favourite_database = favourite_imported.inject_substitute_in_favourite(substitute_selected_data)

        context = {"favourite_database": favourite_database}
        return render(request, 'purbeurre_website/display_favourite.html', context)


def display_product_data(request):
    if request.method == "POST":
        product_selected_id = request.POST.get('product_selected_id')

        product_imported = ProductImporter()
        product_selected_data = product_imported.retrieve_product_data_from_database(product_selected_id)

        context = {"product_selected_data": product_selected_data}
        return render(request, 'purbeurre_website/display_product_data.html', context)


def display_substitute_data(request):
    if request.method == "POST":
        substitute_selected_name = request.POST.get('substitute_selected_name')
        substitute_selected_data = request.POST.get('substitute_selected_data')
        substitute_selected_data = ast.literal_eval(substitute_selected_data)

        context = {
            "substitute_selected_name": substitute_selected_name,
            "substitute_selected_data": substitute_selected_data
        }
        return render(request, 'purbeurre_website/display_substitute_data.html', context)


def display_searched_results(request):
    category_imported = CategoryImporter()
    category_list = category_imported.load_category()
    category_database = category_imported.inject_category_in_database(category_list)
    category_imported.paginate_category_url(category_list)

    if request.method == "POST":
        searched_product_name = request.POST.get('searched_product_name')

        searched_product_imported = ProductImporter()
        searched_products_url = searched_product_imported.load_products_url(searched_product_name)

        products_list = searched_product_imported.extract_products(searched_products_url)
        product_database = searched_product_imported.inject_product_in_database(products_list, category_database)

        if len(products_list) == 0:
            messages.info(request, "Il n'y a pas de produit correspondant à votre recherche.")
            return redirect('home')

        context = {
            "searched_product_name": searched_product_name,
            "product_database": product_database}

        return render(request, 'purbeurre_website/display_searched_results.html', context)


def display_proposed_substitute(request):
    if request.method == "POST":
        product_selected_id = request.POST.get('product_selected_id')

        product_selected_data = ProductImporter()
        product_selected_data = product_selected_data.retrieve_product_data_from_database(product_selected_id)

        # We fetch the category of the product selected
        category_imported = CategoryImporter()
        product_selected_category = category_imported.category_table.get(
            category_id=product_selected_data.category_id.category_id).category_name

        # We fetch the products of this category
        product_imported = ProductImporter()
        substitute_url_list = product_imported.load_products_url(product_selected_category)

        # We filter the products of the list so as to have a substitute list
        substitute_list = product_imported.extract_products(substitute_url_list)
        substitute_list = product_imported.propose_substitute(product_selected_data, substitute_list)

        context = {
            "product_selected_data": product_selected_data,
            "substitute_list": substitute_list,
        }
        return render(request, 'purbeurre_website/display_proposed_substitute.html', context)


@login_required(login_url='login')
def home(request):
    return render(request, 'purbeurre_website/home.html')


def logout_user(request):
    logout(request)
    return redirect('login')


def delete_product(request):
    if request.method == "POST":
        substitute_selected_id = request.POST.get('substitute_selected_id')
        print(substitute_selected_id)
        print(type(substitute_selected_id))

        substitute_deleted = ProductEliminator()
        substitute_deleted = substitute_deleted.delete_substitute(substitute_selected_id)
        print(substitute_deleted)

    return render(request, 'purbeurre_website/display_favourite.html')
