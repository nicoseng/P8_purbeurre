from purbeurre_website.models import Category, Product


class ProductInjectorInTable:
    """To inject products datas in category table """

    @staticmethod
    def inject_product_in_table(product_list, category_table):

        product_table = Product.objects.all()
        product_table.delete()

        for product in product_list:
            for category in category_table:

                if category.category_name in product["categories"]:

                    category_key = Category(category.category_id)
                    product_data = Product(
                        category_key=category_key,
                        product_name=product["product_name"],
                        product_nutriscore=product["nutriscore"],
                        product_image=product["product_image"],
                        product_url=product["url"]
                    )
                    product_data.save()

            for row in product_table.reverse():
                if Product.objects.filter(product_name=row.product_name).count() > 1:
                    row.delete()

        return product_table
