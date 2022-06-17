"""Internal imports"""


class SubstituteExtractor:

    @staticmethod
    def get_substitute(products_list, product_selected_data):

        available_nutriscore_list = ["a", "b", "c", "d", "e"]
        selected_product_nutriscore = product_selected_data["nutriscore"]
        selected_nutriscore_index = \
            available_nutriscore_list.index(selected_product_nutriscore)
        best_nutriscore_list = \
            available_nutriscore_list[0:selected_nutriscore_index]

        available_best_products_list = []
        for product in products_list:
            if product["nutriscore"] in best_nutriscore_list or product["nutriscore"] == "a":

                best_product_dict = {"product_name": product["product_name"],
                                     "nutriscore": product["nutriscore"],
                                     "product_image": product["product_image"],
                                     "ingredients": product["ingredients"],
                                     "url": product["url"]}

                available_best_products_list.append(best_product_dict)

            # if len(available_best_products_list) == 0:
            #     print("Cet article possède déjà le meilleur nutriscore possible de la catégorie.")

            else:
                substitute_proposed_list = available_best_products_list

        return substitute_proposed_list
