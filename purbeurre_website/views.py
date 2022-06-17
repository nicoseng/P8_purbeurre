import ast

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from requests import exceptions, get
from urllib3.util import retry

from .category_loader import CategoriesLoader
from .forms import CreateUser
from .models import Substitute, Basket, Product, Category
from .product_extractor import ProductExtractor
from .category_extractor import CategoriesExtractor
from .substitute_extractor import SubstituteExtractor


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
            print("je suis là")
            print(row)
            if substitute_selected_data.substitute_url == row.substitute_url:
                print("Vous avez déjà enregsitré ce produit")
            else:
                print("Produit bien enregistré ")
                substitute_selected_data.save()

        table_displayed = Substitute.objects.all()
        print(table_displayed)
        context = {"table_displayed": table_displayed}

    return render(request, 'purbeurre_website/check_my_basket.html', context)


def check_product(request):
    if request.method == "POST":
        product_selected_data = request.POST.get('product_selected_data')
        print(product_selected_data)
        product_selected_data = ast.literal_eval(product_selected_data)
        print(product_selected_data)

        print(product_selected_data["product_name"])
        context = {"product_selected_data": product_selected_data}
        return render(request, 'purbeurre_website/check_product.html', context)


def check_substitute(request):
    if request.method == "POST":
        substitute_selected = request.POST.get('substitute_selected')
        print(substitute_selected)
        substitute_selected_data = request.POST.get('substitute_selected_data')
        #substitute_selected_data = ast.literal_eval(substitute_selected_data)
        print(substitute_selected_data)
        print(type(substitute_selected_data))
        #print(substitute_selected_data.substitute_url)
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

        products_data = searched_product_data.extract_products(searched_products_url)

        if len(products_data) == 0:
            messages.info(request, "Il n'y a pas de produit correspondant à votre recherche.")
            return redirect('home')

        else:
            category_list = CategoriesLoader()
            category_list = category_list.load_categories()
            print(category_list)
            category_table = Category.objects.all()
            category_table.delete()

            for category in category_list:
                category_data = Category(
                    category_name=category["category_name"],
                    category_url=category["url"]
                )
                category_data.save()

            # for category in category_list:
            #     try:
            #         category_data = Category(
            #             category_name=category["category_name"],
            #             category_url=category["url"]
            #         )
            #         category_data.save()
            #     except KeyError:
            #         continue

            # except exceptions.RequestException:
            #
            #     if retry > 0:
            #         return display_results(retry - 1)

            product_table = Product.objects.all()
            product_table.delete()
            for product in products_data:

                if product["product_name"] != Product.product_name:
                    product_data = Product(
                        product_name=product["product_name"],
                        product_nutriscore=product["nutriscore"],
                        product_image=product["product_image"],
                        product_url=product["url"]
                    )
                    product_data.save()

            for product in product_table.reverse():
                if Product.objects.filter(product_name=product.product_name).count() > 1:
                    product.delete()

            for element in product_table:
                print(element.product_name)

            # context = {
            #     "product_selected": product_selected,
            #     "product_selected_data": product_selected_data,
            #     "substitute_proposed_list": substitute_proposed_list,
            #     "substitute_table": substitute_table
            # }
            # return render(request, 'purbeurre_website/display_substitute.html', context)
            context = {"product_name": searched_product_name,
                       "products": product_table
                       }
            return render(request, 'purbeurre_website/display_results.html', context)


def display_substitute(request):
    if request.method == "POST":
        product_selected = request.POST.get('product_selected')
        product_selected_data = request.POST.get('product_selected_data')
        # product_selected_data = ast.literal_eval(product_selected_data)

        product_selected_id = request.POST.get('product_selected_id')

        # Récupérer la catégorie du produit sélectionné
        # product_selected_category = product_selected_data["categories"]
        product_selected_category = product_selected_category.split(",")

        category_extracted = CategoriesExtractor()
        categories_list_url = category_extracted.extract_categories_url(product_selected_category)

        products_list = ProductExtractor()
        products_list = products_list.extract_products(categories_list_url)

        substitute_proposed_list = SubstituteExtractor()
        substitute_proposed_list = substitute_proposed_list.get_substitute(products_list, product_selected_data)

        substitute_table = Substitute.objects.all()
        substitute_table.delete()

        for substitute in substitute_proposed_list:

            if substitute["product_name"] != Substitute.substitute_name:

                substitute_selected_data = Substitute(
                    reference_product_key= product_selected_id,
                    substitute_name=substitute["product_name"],
                    substitute_nutriscore=substitute["nutriscore"],
                    substitute_image=substitute["product_image"],
                    substitute_url=substitute["url"]
                )
                substitute_selected_data.save()

        for substitute in substitute_table.reverse():
            if Substitute.objects.filter(substitute_name=substitute.substitute_name).count() > 1:
                substitute.delete()

        for element in substitute_table:
            print(element.substitute_name)



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
