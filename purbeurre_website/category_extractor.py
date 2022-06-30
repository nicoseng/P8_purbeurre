"""Internal imports """
from requests import get, exceptions


class CategoriesExtractor:
    """To extract categories datas loaded from the API OpenFoodFacts(OFF)."""
    @staticmethod
    def extract_categories_url(category_name, retry=3):
        """Extracts a list with each category datas."""

        categories_list_url = []
        nb_of_page = range(0, 1)
        # nb_of_page = range(ceil(category_page_json["count"]/category_page_json["page_size"]))
        for page in nb_of_page:

            while page <= len(nb_of_page):

                try:

                    #category_name = "+".join(category_name)
                    category_url = "https://fr.openfoodfacts.org/cgi/search.pl?json=1&action=process" \
                                   "&search_simple=1&search_terms=" + str(category_name) + "&page=" + str(page)
                    categories_list_url.append(category_url)

                except exceptions.RequestException:

                    if retry <= 0:
                        return CategoriesExtractor.extract_categories_url(category_name)
                page += 1

            return categories_list_url
