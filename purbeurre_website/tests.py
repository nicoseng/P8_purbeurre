from django.test import TestCase

# Create your tests here.
from requests import get, exceptions
from urllib3.util import retry

from purbeurre_website.category_loader import CategoriesLoader


def load_categories():
    categories_loaded_list = []

    try:

        categories_url = "https://fr.openfoodfacts.org/categories&json=1"
        request = get(categories_url)

        # To get the json format
        categories_url_json = request.json()

        # We chose to fetch 10 categories for example
        for category in categories_url_json["tags"][:10]:
            category_dict = {
                "category_name": category["name"],
                "category_url": category["url"]
            }
            categories_loaded_list.append(category_dict)

    except exceptions.RequestException:

        if retry > 0:
            return CategoriesLoader.load_categories(retry - 1)

    return categories_loaded_list


class CategoriesLoaderTests(TestCase):
    pass
