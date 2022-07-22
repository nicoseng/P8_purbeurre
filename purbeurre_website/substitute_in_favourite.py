from urllib import request

from django.contrib.auth.models import User

from purbeurre_website.models import Favourite


class SubstituteInFavourite:
    """To inject products datas in favourite database """

    @staticmethod
    def inject_substitute_in_favourite(substitute_selected_data, user_id):

        favourite_database = Favourite.objects.all()

        if Favourite.objects.filter(substitute_name=substitute_selected_data["product_name"]).exists():
            message = "Vous avez déjà ajouté {} dans vos favoris.".format(substitute_selected_data["product_name"])
            return message

        else:

            substitute_selected_data = Favourite(
                user_id=user_id.user_id,
                substitute_name=substitute_selected_data["product_name"],
                substitute_image=substitute_selected_data["product_image"],
                substitute_nutriscore=substitute_selected_data["nutriscore"]
            )
            substitute_selected_data.save()
            favourite_database.update()

        return favourite_database
