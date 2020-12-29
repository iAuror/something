from django.core.management import BaseCommand

from manager.models import Comment, Books, BookRating, TMPBooks


class Command(BaseCommand):
    def handle(self, *args, **options):
        books=Books.objects.all()
        arr=[TMPBooks(
                title=i.title,
                text=i.text,
                published=i.published,
                shop=i.shop,
                genre=i.genre,
                rate=i.rate,
                count_rate_users=i.count_rate_users,
                rate_all_stars=i.rate_all_stars,
                slug=i.slug,
            )
            for i in books
        ]
        TMPBooks.objects.bulk_create(arr)
        rate_slug=Books.objects.all().values('slug','id')
        rate=BookRating.objects.all()
        for q in rate_slug:
            new_r=rate.filter(book_id=q['id'])
            for qwe in new_r:
                qwe.tmp_book_id=q['slug']
                qwe.save()
                #BookRating.objects.bulk_update(rate,['tmp_book_id'])

        comment = Books.objects.all().values('id', 'slug')
        tmp_com = Comment.objects.all()
        for l in comment:
            temp = tmp_com.filter(book_id=l['id'])
            for i in temp:
                i.tmp_book_id = l['slug']
                i.save()
            #Comment.objects.bulk_update(tmp_com,['tmp_book_id'])

        books=Books.objects.all()
        tmp_books=TMPBooks.objects.all()
        for i in books:
            tmpbook=tmp_books.get(slug=i.slug)
            for q in i.author.all():
                tmpbook.author.add(q)
            tmpbook.save()
