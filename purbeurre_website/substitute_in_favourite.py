from purbeurre_website.models import Favourite


class SubstituteInFavourite:
    """To inject products datas in favourite database """

    @staticmethod
    def inject_substitute_in_favourite(substitute_selected_data):

        favourite_database = Favourite.objects.all()

        if Favourite.objects.filter(substitute_name=substitute_selected_data["product_name"]).exists():
            message = "Vous avez déjà ajouté {} dans vos favoris.".format(substitute_selected_data["product_name"])
            print(message)

        else:
            substitute_selected_data = Favourite(
                # user_id=User.objects.get(user_id=user_id),
                substitute_name=substitute_selected_data["product_name"],
                substitute_image=substitute_selected_data["product_image"],
                substitute_nutriscore=substitute_selected_data["nutriscore"]
            )
            substitute_selected_data.save()
            favourite_database.update()

        return favourite_database

    @staticmethod
    def retrieve_substitute_from_table(substitute_table):

        substitute_list_from_table = []
        for substitute in substitute_table:
            substitute_dict = {

                "category_key": substitute.category_key.category_id,
                "substitute_id": substitute.substitute_id,
                "substitute_name": substitute.substitute_name,
                "nutriscore": substitute.substitute_nutriscore,
                "substitute_image": substitute.substitute_image,
                "url": substitute.substitute_url,
                "ingredients": substitute.substitute_ingredients
            }

            substitute_list_from_table.append(substitute_dict)

        return substitute_list_from_table
