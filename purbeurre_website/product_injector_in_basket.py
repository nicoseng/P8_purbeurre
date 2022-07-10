from purbeurre_website.models import Basket


class ProductInjectorInBasket:
    """To inject products datas in basket table """

    @staticmethod
    def inject_substitute_in_basket(substitute_selected_data):
        basket_list = Basket.objects.all()

        if Basket.objects.filter(substitute_name=substitute_selected_data["substitute_name"]).exists():
            print("le produit existe déjà dans votre panier.On en va pas l'ajouter")

        else:
            new_substitute_added = Basket(
                substitute_name=substitute_selected_data["substitute_name"],
                substitute_nutriscore=substitute_selected_data["nutriscore"],
                substitute_image=substitute_selected_data["substitute_image"],
                substitute_url=substitute_selected_data["url"]
            )
            new_substitute_added.save()

            print(new_substitute_added.substitute_name)
            print(substitute_selected_data["substitute_name"])
            print("Produit bien ajouté dans votre panier.")

        basket_list.update()
        return basket_list
