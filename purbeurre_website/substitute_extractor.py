"""Internal imports"""


class SubstituteExtractor:

    @staticmethod
    def get_substitute(products_list, product_selected_data):

        available_nutriscore_list = ["a", "b", "c", "d", "e"]

        selected_nutriscore_index = \
            available_nutriscore_list.index(product_selected_data["nutriscore"])
        best_nutriscore_list = \
            available_nutriscore_list[0:selected_nutriscore_index]

        substitute_proposed_list = []
        for product in products_list:
            if product["nutriscore"] in best_nutriscore_list or product["nutriscore"] == "a":

                best_product_dict = {"product_category": product["categories"],
                                     "product_name": product["product_name"],
                                     "nutriscore": product["nutriscore"],
                                     "product_image": product["product_image"],
                                     "ingredients": product["ingredients"],
                                     "url": product["url"]
                                     }

                substitute_proposed_list.append(best_product_dict)

        return substitute_proposed_list
