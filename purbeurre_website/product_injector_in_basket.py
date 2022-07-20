from purbeurre_website.models import Basket, Category


class ProductInjectorInBasket:
    """To inject products datas in basket table """

    @staticmethod
    def inject_substitute_in_basket(substitute_selected_data):
        basket_list = Basket.objects.all()

        if Basket.objects.filter(substitute_name=substitute_selected_data["substitute_name"]).exists():
            print("le produit existe déjà dans votre panier.On ne va pas l'ajouter")

        else:
            for substitute in substitute_selected_data:
                new_substitute_added = Basket(
                    category_key=Category.objects.get(category_id=substitute["category_key"]),
                    substitute_name=substitute["substitute_name"],
                    substitute_nutriscore=substitute["nutriscore"],
                    substitute_image=substitute["substitute_image"],
                    substitute_url=substitute["url"],
                    substitute_ingredients=substitute["ingredients"]
                )
                new_substitute_added.save()

                print(new_substitute_added.substitute_name)
                print(substitute_selected_data["substitute_name"])
                print("Produit bien ajouté dans votre panier.")

        basket_list.update()
        return basket_list

    @staticmethod
    def retrieve_substitute_from_basket(basket_list):

        basket_list_from_table = []
        for substitute in basket_list:
            substitute_dict = {

                "category_key": substitute.category_key.category_id,
                "category_name": substitute.category_key.category_name,
                "substitute_id": substitute.substitute_id,
                "substitute_name": substitute.substitute_name,
                "nutriscore": substitute.substitute_nutriscore,
                "substitute_image": substitute.substitute_image,
                "url": substitute.substitute_url,
                "ingredients": substitute.substitute_ingredients
            }

            basket_list_from_table.append(substitute_dict)

        return basket_list_from_table
