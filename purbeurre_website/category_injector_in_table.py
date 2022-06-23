from purbeurre_website.category_loader import CategoriesLoader
from purbeurre_website.models import Category


class CategoryInjectorInTable:
    """To inject categories datas in category table """


    @staticmethod
    def inject_category_in_table(category_list):

        category_table = Category.objects.all()
        category_table.delete()

        for category in category_list:
            category_data = Category(
                category_name=category["category_name"],
                category_url=category["category_url"]
            )
            category_data.save()

        return category_table
