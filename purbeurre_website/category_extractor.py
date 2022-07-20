"""Internal imports """
from requests import exceptions


class CategoriesExtractor:
    """To extract categories datas loaded from the API OpenFoodFacts(OFF)."""

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

            # We chose to fetch 10 categories for example
            for category in categories_url_json["tags"][:10]:
                category_dict = {
                    "category_name": category["name"],
                    "category_url": category["url"]
                }
                categories_loaded_list.append(category_dict)

        except exceptions.RequestException:

            if retry > 0:
                return CategoryImporter.load_categories(retry - 1)

        return categories_loaded_list

    def extract_category_url(self):
        pass

    def inject_category_in_database(self):
        pass

    @staticmethod
    def extract_categories_url(category_name, retry=3):
        """Extracts a list with each category datas."""

        categories_list_url = []
        nb_of_page = range(0, 1)
        # nb_of_page = range(ceil(category_page_json["count"]/category_page_json["page_size"]))
        for page in nb_of_page:

            while page <= len(nb_of_page):

                try:

                    category_url = "https://fr.openfoodfacts.org/cgi/search.pl?json=1&action=process" \
                                   "&search_simple=1&search_terms=" + str(category_name) + "&page=" + str(page)
                    categories_list_url.append(category_url)

                except exceptions.RequestException:

                    if retry <= 0:
                        return CategoriesExtractor.extract_categories_url(category_name)
                page += 1

            return categories_list_url

