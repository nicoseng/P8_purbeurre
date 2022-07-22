from django.core.management.base import BaseCommand

from purbeurre_website.category_importer import CategoryImporter
from purbeurre_website.models import Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            category_imported = CategoryImporter()
            category_list = category_imported.load_category()
            category_imported.inject_category_in_database(category_list)
            category_imported.paginate_category_url(category_list)

        except Category.DoesExist:
            Category.objects.all()

        self.stdout.write("Categories OFF bien importées.")
