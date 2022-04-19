"""Internal imports"""

from requests import get, exceptions


class ProductExtractor:
    """
    Extracts products from the API OpenFoodFacts(OFF).
    """
    @staticmethod
    def extract_products(product_name, retry=3):
        """
        This function extracts the products datas

        from the URL address in OFF.

        Parameters
        ----------
        retry : type int
            The number of attempts if there are errors.

        product_name : type str
            The name of the product

        """
        products_loaded_list = []

        try:

            product_url = "https://fr.openfoodfacts.org/cgi/search.pl?json=1&action=process&search_simple=1&search_terms="+ product_name
            request = get(product_url)

            # To get the json format
            products_url_json = request.json()

            for product in products_url_json["products"]:
                products_loaded_list.append(product["product_name_fr"])

        except exceptions.RequestException:

            if retry > 0:
                return ProductExtractor.extract_products(retry - 1)

        return products_loaded_list