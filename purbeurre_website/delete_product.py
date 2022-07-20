# from purbeurre_website.models import Basket


class ProductEraserInBasket:
    """To inject products datas in basket table """

    @staticmethod
    def delete_substitute_in_basket(substitute_selected_data):
        basket_list = Basket.objects.all()
        delete_row = Basket.objects.get(substitute_id=substitute_selected_data["substitute_id"])
        delete_row.delete()

        basket_list.update()
        return basket_list
