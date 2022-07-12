from purbeurre_website.models import Category, Product


class ProductInjectorInTable:
    """To inject products datas in category table """

    @staticmethod
    def inject_product_in_table(product_list, category_table):

        product_table = Product.objects.all()

        for product in product_list:
            for category in category_table:

                if category.category_name in product["categories"]:

                    category_key = Category(category.category_id)
                    product_data = Product(
                        category_key=category_key,
                        product_name=product["product_name"],
                        product_nutriscore=product["nutriscore"],
                        product_image=product["product_image"],
                        product_ingredients=product["ingredients"],
                        product_url=product["url"]
                    )
                    product_data.save()

        return product_table

    @staticmethod
    def retrieve_product_from_table(product_table):

        products_list_from_table = []
        for product in product_table:
            product_dict = {
                            "category_key": product.category_key.category_id,
                            "category_name": product.category_key.category_name,
                            "product_id": product.product_id,
                            "product_name": product.product_name,
                            "nutriscore": product.product_nutriscore,
                            "product_image": product.product_image,
                            "url": product.product_url,
                            "ingredients": product.product_ingredients
                            }

            products_list_from_table.append(product_dict)

        return products_list_from_table
