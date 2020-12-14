from django.core.management import BaseCommand
from manager.models import Books
from slugify import slugify


class Command(BaseCommand):
    def handle(self, *args, **options):
        books = Books.objects.all()
        for i in books:
            i.slug = slugify(i.title)
            try:
                i.save()
            except:
                i.slug += str(i.id)
                i.save
