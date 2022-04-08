"""Internal imports """

from category_loader import CategoriesLoader


class CategoriesExtractor:
    """To extract categories datas loaded from the API OpenFoodFacts(OFF)."""
    @staticmethod
    def extract_categories_datas():
        """Extracts a list with each category datas."""

        categories_loaded_list = CategoriesLoader.load_categories()

        categories_extracted_list = []

        for category in categories_loaded_list:

            # We create an empty dictionnary to stock it in the category list.
            category_extracted_dict = {"category_name": ""}
            category_extracted_dict["category_name"] = category["name"]
            categories_extracted_list.append(category_extracted_dict)

        return categories_extracted_list
