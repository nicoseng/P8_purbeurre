from purbeurre_website.category_loader import CategoriesLoader
from purbeurre_website.models import Category, Product


class ProductInjectorInTable:
    """To inject products datas in category table """

    @staticmethod
    def inject_product_in_table(product_list):

        product_table = Product.objects.all()
        product_table.delete()

        for product in product_list:
            if product["product_name"] != Product.product_name:
                product_data = Product(
                    product_name=product["product_name"],
                    product_nutriscore=product["nutriscore"],
                    product_image=product["product_image"],
                    product_url=product["url"]
                )
                product_data.save()

        for product in product_table.reverse():
            if Product.objects.filter(product_name=product.product_name).count() > 1:
                product.delete()

        return product_table
