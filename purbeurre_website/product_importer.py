"""Internal imports"""
from typing import List, Any

from requests import get, exceptions
from purbeurre_website.models import Category, Product


class ProductImporter:
    """
    Import category of products from the API OpenFoodFacts(OFF) and insert it in the database.
    """

    def __init__(self):

        self.product_database = Product.objects.all()
        self.product_data = {}
        self.product_url_list = []
        self.products_list = []
        self.substitute_data = {}
        self.substitute_proposed_list = []

    def load_products_url(self, product_name, retry=3):

        """
        Extracts products URLS from the API OpenFoodFacts(OFF).
        """

        nb_of_page = range(0, 1)
        for page in nb_of_page:

            while page <= len(nb_of_page):

                try:
                    product_name.split()
                    product_name = "".join(product_name)
                    product_url = "https://fr.openfoodfacts.org/cgi/search.pl?json=1&action=process&search_simple=1" \
                                  "&search_terms={}&page={}".format(product_name, str(page))
                    self.product_url_list.append(product_url)

                except exceptions.RequestException:

                    if retry <= 0:
                        return ProductImporter.load_products_url(product_name)
                page += 1

            return self.product_url_list

    def extract_products(self, products_list_url):

        """
        To extract the products from url of the products.
        :param products_list_url: list of product URLS
        """
        for url in products_list_url:

            try:
                print(url)
                product_page_url = get(url)
                product_page_json = product_page_url.json()
                number = 0
                page_count = product_page_json["page_count"]
                while number < page_count:
                    self.product_data = {"categories": "",
                                         "product_name": "",
                                         "nutriscore": "",
                                         "product_image": "",
                                         "url": "",
                                         "ingredients": ""
                                         }

                    product_category = product_page_json["products"][number]["categories"]
                    self.product_data["categories"] = product_category

                    product_image = product_page_json["products"][number]["image_small_url"]
                    self.product_data["product_image"] = product_image

                    product_name = product_page_json["products"][number]["product_name_fr"]
                    self.product_data["product_name"] = product_name

                    nutriscore = product_page_json["products"][number]["nutrition_grade_fr"]
                    self.product_data["nutriscore"] = nutriscore

                    url = product_page_json["products"][number]["url"]
                    self.product_data["url"] = url

                    ingredients = product_page_json["products"][number]["ingredients_text_fr"]
                    self.product_data["ingredients"] = ingredients

                    self.products_list.append(self.product_data)
                    number += 1

            # To avoid empty field from OpenFoodFacts
            except KeyError:
                pass
            except IndexError:
                pass

        return self.products_list

    def inject_product_in_database(self, products_list, category_table):

        self.product_database.delete()

        for product in products_list:
            for category in category_table:

                if category.category_name in product["categories"]:
                    category_id = Category(category.category_id)
                    product_data = Product(
                        category_id=category_id,
                        product_name=product["product_name"],
                        product_nutriscore=product["nutriscore"],
                        product_image=product["product_image"],
                        product_ingredients=product["ingredients"],
                        product_url=product["url"]
                    )
                    product_data.save()

        return self.product_database

    @staticmethod
    def retrieve_product_data_from_database(product_selected_id):

        product_selected_data = Product.objects.get(product_id=product_selected_id)
        return product_selected_data

    def propose_substitute(self, product_selected_data, product_list):

        product_selected_nutriscore = product_selected_data.product_nutriscore
        available_nutriscore_list = ["a", "b", "c", "d", "e"]
        selected_nutriscore_index = \
            available_nutriscore_list.index(product_selected_nutriscore)
        best_nutriscore_list = \
            available_nutriscore_list[0:selected_nutriscore_index]

        for product in product_list:
            if product["nutriscore"] in best_nutriscore_list or product["nutriscore"] == "a":
                self.substitute_data = {
                    "product_name": product["product_name"],
                    "nutriscore": product["nutriscore"],
                    "product_image": product["product_image"],
                    "ingredients": product["ingredients"],
                    "url": product["url"]
                }

                self.substitute_proposed_list.append(self.substitute_data)

        return self.substitute_proposed_list
