"""Internal imports"""
from requests import get, exceptions
from purbeurre_website.models import Category


class CategoryImporter:
    """
    Import category of products from the API OpenFoodFacts(OFF) and insert it in the database.
    """

    def __init__(self):
        self.category_table = Category.objects.all()
        self.category_data = {}
        self.category_list = []
        self.category_url_list = []

    def load_category(self, retry=3):
        """
        Loads the categories datas

        from the URL address in OFF.

        Parameters
        ----------
        retry : type int
            The number of attempts if there are errors.

        """
        try:

            categories_url = "https://fr.openfoodfacts.org/categories&json=1"
            request = get(categories_url)

            # To get the json format
            categories_url_json = request.json()

            # We chose to fetch 10 categories for example
            for category in categories_url_json["tags"][:10]:
                self.category_data = {
                    "category_name": category["name"],
                    "category_url": category["url"]
                }
                self.category_list.append(self.category_data)

        except exceptions.RequestException:

            if retry > 0:
                return CategoryImporter.load_category(retry - 1)

        return self.category_list

    def inject_category_in_database(self, category_list):

        self.category_table.delete()

        for category in category_list:
            category_data = Category(
                category_name=category["category_name"],
                category_url=category["category_url"]
            )
            category_data.save()

        return self.category_table

    def paginate_category_url(self, category_list, retry=3):

        """Aims to fetch each category URL link per page"""
        for category in category_list:
            category_url = category["category_url"]

            nb_of_page = range(0, 1)
            for page in nb_of_page:
    
                while page <= len(nb_of_page):
    
                    try:
                        category_url_page = "{}&json=1&page={}".format(category_url, str(page))
                        self.category_url_list.append(category_url_page)
    
                    except exceptions.RequestException:
    
                        if retry <= 0:
                            return CategoryImporter.extract_category_url(self, category_list)
                    page += 1

        return self.category_url_list


