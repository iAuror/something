from django.core.management import BaseCommand
from django.db.models import Count

from manager.models import Comment


class Command(BaseCommand):
    def handle(self, *args, **options):
        comment=Comment.objects.annotate(tmp_like=Count('likes'))
        for i in comment:
            i.likes_count=i.tmp_like
        Comment.objects.bulk_update(comment,('likes_count',))