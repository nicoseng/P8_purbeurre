from purbeurre_website.models import Basket


class ProductEraserInBasket:
    """To inject products datas in basket table """

    @staticmethod
    def delete_substitute_in_basket(basket_list):
        basket_list = Basket.objects.all()
        instance = Basket.objects.get(substitute_id=id)
        instance.delete()



        basket_list.update()
        return basket_list
