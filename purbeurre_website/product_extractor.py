"""Internal imports"""
from math import ceil

from requests import get, exceptions
from urllib3.util import retry


class ProductExtractor:

    @staticmethod
    def extract_products_url(product_name, retry=3):

        """
        Extracts products URLS from the API OpenFoodFacts(OFF).
        """

        products_list_url = []
        product_url = "https://fr.openfoodfacts.org/cgi/search.pl?json=1&action=process&search_simple=1" \
                      "&search_terms=" + str(product_name)
        product_page_url = get(product_url)
        product_page_json = product_page_url.json()
        nb_of_page = range(ceil(product_page_json["count"]/product_page_json["page_size"]))
        print(nb_of_page)
        for page in nb_of_page:

            while page <= len(nb_of_page):

                try:
                    product_name = product_name.split()
                    product_name = "+".join(product_name)
                    product_url = "https://fr.openfoodfacts.org/cgi/search.pl?json=1&action=process&search_simple=1" \
                                  "&search_terms=" + product_name + "&page=" + str(page)
                    products_list_url.append(product_url)

                except exceptions.RequestException:

                    if retry <= 0:
                        return ProductExtractor.extract_products_url(product_name)
                page += 1

            return products_list_url

    @staticmethod
    def extract_products(products_list_url):

        """
        To extract the product url.
        :param products_list_url: list of product URLS
        """
        products_list = []
        print(products_list_url)
        for url in products_list_url:

            try:
                #print(url)
                product_page_url = get(url)
                product_page_json = product_page_url.json()
                number = 0
                page_count = product_page_json["page_count"]
                while number < page_count:

                    page_count = product_page_json["page_count"]

                    product_dict = {"product_name": "", "nutriscore": "", "id":""}

                    product_id = product_page_json["products"][number]["_id"]
                    product_dict["id"] = product_id

                    product_name = product_page_json["products"][number]["product_name"]
                    product_dict["product_name"] = product_name

                    nutriscore = product_page_json["products"][number]["nutrition_grade_fr"]
                    product_dict["nutriscore"] = nutriscore

                    products_list.append(product_dict)
                    number += 1

            # To avoid empty field from OpenFoodFacts
            except KeyError:
                pass
            except IndexError:
                pass
        print(len(products_list))
        return products_list
