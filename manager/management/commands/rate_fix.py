from django.core.management import BaseCommand
from django.db.models import Sum, Count

from manager.models import Books


class Command(BaseCommand):
    def handle(self, *args, **options):
        books = Books.objects.annotate(tmp_all_stars=Sum('user_rate__rate'),
                                       tmp_rate_users=Count('user_rate'),
                                       )
        for i in books:
            i.rate_all_stars = i.tmp_all_stars
            i.count_rate_users = i.tmp_rate_users
            i.rate = i.rate_all_stars / i.count_rate_users
        Books.objects.bulk_update(books, ['rate_all_stars', 'count_rate_users', 'rate'])
