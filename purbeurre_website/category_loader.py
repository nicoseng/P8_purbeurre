"""Internal imports"""

from requests import get, exceptions
from urllib3.util import retry


class CategoryExtractor:
    """
    Loads categories of products from the API OpenFoodFacts(OFF).
    """
    @staticmethod
    def load_categories(retry=3):
        """
        This function loads the categories datas

        from the URL address in OFF.

        Parameters
        ----------
        retry : type int
            The number of attempts if there are errors.

        """
        categories_loaded_list = []

        try:

            categories_url = "https://fr.openfoodfacts.org/categories&json=1"
            request = get(categories_url)

            # To get the json format
            categories_url_json = request.json()

            for category in categories_url_json["tags"]:
                categories_loaded_list.append(category["name"])

        except exceptions.RequestException:

            if retry > 0:
                return CategoryExtractor.load_categories(retry - 1)

        return categories_loaded_list

