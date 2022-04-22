"""Internal imports"""

from requests import get, exceptions
from urllib3.util import retry


class ProductExtractor:

    @staticmethod
    def extract_products_url(product_name):

        """
        Extracts products URLS from the API OpenFoodFacts(OFF).
        """

        products_list_url = []
        nb_of_page = range(0,1)
        for page in nb_of_page:

            while page <= max(nb_of_page):

                try:

                    product_url = "https://fr.openfoodfacts.org/cgi/search.pl?json=1&action=process&search_simple=1" \
                                  "&search_terms=" + product_name + "&page=" + str(page)
                    products_list_url.append(product_url)

                except exceptions.RequestException:

                    if retry <= 0:
                        return ProductExtractor.extract_products_url(product_name)
                page += 1
        print(products_list_url)
        return products_list_url

    @staticmethod
    def extract_products(products_list_url, start_product_nb, page_count):

        """To extract the product url.

                :param start_product_nb: Indicate the numbers of position of the products
                :param last_product_nb: The last number of the interval.
                :param products_list_url: list of product URLS

        """

        products_list = []

        for url in products_list_url:
            while start_product_nb <= page_count:

                try:
                    product_page_url = get(url)
                    product_page_json = product_page_url.json()

                    product_dict = {"product_name": "", "nutriscore": ""}

                    product_name = product_page_json["products"][
                        start_product_nb]["product_name"]
                    product_dict["product_name"] = product_name

                    nutriscore = product_page_json["products"][
                        start_product_nb]["nutrition_grade_fr"]
                    product_dict["nutriscore"] = nutriscore

                    products_list.append(product_dict)

                # To avoid empty field from OpenFoodFacts
                except KeyError:
                    pass
                except IndexError:
                    pass

            start_product_nb += 1
        print(products_list)
