from purbeurre_website.models import Product, Substitute


class SubstituteInjectorInTable:
    """To inject products datas in category table """

    @staticmethod
    def inject_substitute_in_table(substitute_proposed_list):

        substitute_table = Substitute.objects.all()
        substitute_table.delete()

        for substitute in substitute_proposed_list:
            substitute_selected_data = Substitute(

                substitute_name=substitute["product_name"],
                substitute_nutriscore=substitute["nutriscore"],
                substitute_image=substitute["product_image"],
                substitute_ingredients=substitute["ingredients"],
                substitute_url=substitute["url"]
            )
            substitute_selected_data.save()

        return substitute_table
