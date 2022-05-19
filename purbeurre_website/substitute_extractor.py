"""Internal imports"""
import random


class SubstituteExtractor:

    @staticmethod
    def get_substitute(product_selected):
        print(product_selected)
        print(type(product_selected))

        print(product_selected[0:3])
        available_nutriscore_list = ["a", "b", "c", "d", "e"]
        selected_product_nutriscore = product_selected["nutriscore"]
        selected_nutriscore_index = \
            available_nutriscore_list.index(selected_product_nutriscore)
        best_nutriscore_list = \
            available_nutriscore_list[0:selected_nutriscore_index]

        available_best_products_list = []
        for product in product_selected:
            if product["nutriscore"] in best_nutriscore_list:

                best_product_dict = {"product_name": product["product_name"], "nutriscore": product["nutriscore"],
                                     "product_image": product["product_image"]}

                available_best_products_list.append(best_product_dict)

            if len(available_best_products_list) == 0:
                print("Cet article possède déjà le meilleur nutriscore possible de la catégorie.")

            else:
                substitute_proposed = random.choice(available_best_products_list)
                return substitute_proposed
