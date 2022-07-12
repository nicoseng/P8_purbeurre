from purbeurre_website.models import Substitute, Category


class SubstituteInjectorInTable:
    """To inject products datas in category table """

    @staticmethod
    def inject_substitute_in_table(substitute_proposed_list, category_table):

        substitute_table = Substitute.objects.all()
        substitute_table.delete()

        for substitute in substitute_proposed_list:
            for category in category_table:
                if category.category_name in substitute["product_category"]:
                    category_key = Category(category.category_id)
                    substitute_selected_data = Substitute(
                        category_key=category_key,
                        substitute_name=substitute["product_name"],
                        substitute_nutriscore=substitute["nutriscore"],
                        substitute_image=substitute["product_image"],
                        substitute_ingredients=substitute["ingredients"],
                        substitute_url=substitute["url"]
                    )
                    substitute_selected_data.save()

        return substitute_table

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
