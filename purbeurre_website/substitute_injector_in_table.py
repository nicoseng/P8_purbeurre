from purbeurre_website.models import Product, Substitute


class SubstituteInjectorInTable:
    """To inject products datas in category table """

    @staticmethod
    def inject_substitute_in_table(substitute_proposed_list, product_table):

        substitute_table = Substitute.objects.all()
        substitute_table.delete()

        for substitute in substitute_proposed_list:
            for product in product_table:

                if product.product_name in substitute["product_name"]:
                    product_key = Product(product.product_id)

                    substitute_selected_data = Substitute(
                        reference_product_key=product_key,
                        substitute_name=substitute["product_name"],
                        substitute_nutriscore=substitute["nutriscore"],
                        substitute_image=substitute["product_image"],
                        substitute_url=substitute["url"]
                    )
                    substitute_selected_data.save()

        for substitute in substitute_table.reverse():
            if Substitute.objects.filter(substitute_name=substitute.substitute_name).count() > 1:
                substitute.delete()

        # product_table = Product.objects.all()
        # product_table.delete()
        #
        # for product in product_list:
        #     for category in category_table:
        #
        #         if category.category_name in product["categories"]:
        #
        #             category_key = Category(category.category_id)
        #             product_data = Product(
        #                 category_key=category_key,
        #                 product_name=product["product_name"],
        #                 product_nutriscore=product["nutriscore"],
        #                 product_image=product["product_image"],
        #                 product_url=product["url"]
        #             )
        #             product_data.save()
        #
        #     for row in product_table.reverse():
        #         if Product.objects.filter(product_name=row.product_name).count() > 1:
        #             row.delete()
        #
        return substitute_table
