from purbeurre_website.models import Basket


class ProductInjectorInBasket:
    """To inject products datas in basket table """

    @staticmethod
    def inject_substitute_in_basket(substitute_selected_data):

        basket_list = Basket.objects.all()
        for substitute in basket_list:

            if substitute.substitute_name in substitute_selected_data["substitute_name"]:
                substitute_selected_data = Basket(
                    substitute_name=substitute_selected_data["substitute_name"],
                    substitute_nutriscore=substitute_selected_data["nutriscore"],
                    substitute_image=substitute_selected_data["substitute_image"],
                    substitute_url=substitute_selected_data["url"]
                )

                substitute_selected_data.save()

        return basket_list
