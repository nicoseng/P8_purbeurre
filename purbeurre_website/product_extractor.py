"""Internal imports"""

from requests import get, exceptions


class ProductExtractor:
    """
    Extracts products from the API OpenFoodFacts(OFF).
    """


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
    nb_of_pages = list(range(10))

    for page in nb_of_pages:
        print(page)
        while page <= len(nb_of_pages):

            try:

                product_url = "https://fr.openfoodfacts.org/cgi/search.pl?json=1&action=process&search_simple=1" \
                              "&search_terms=" + product_name + "&page=" + str(page)
                request = get(product_url)

                # To get the json format
                products_url_json = request.json()

                for product in products_url_json["products"]:
                    products_loaded_list.append(product["product_name_fr"])

            except exceptions.RequestException:

                if retry > 0:
                    return ProductExtractor.extract_products(retry - 1)
            page += 1
            return products_loaded_list
