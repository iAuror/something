from django.db.models import Count
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from manager.models import Books, Comment


def buy(request):
    return HttpResponse('<h1>Временная заглушка</h1>')


class Shop(View):
    def get(self, request):
        books = Books.objects.prefetch_related('shop', 'genre') \
            .annotate(count=Count('likes'), com=Count('comment'))
        context = {'title': 'Shop Book',
                   'name': ['Egor', 'Oleg', 'Anton'],
                   'books': books
                   }
        return render(request, 'manager/index.html', context=context)


class AddLike(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            # book = Books.objects.get(id=id)
            # book.like += 1
            # book.save()
            book = Books.objects.get(id=id)
            if request.user not in book.likes.all():
                book.likes.add(request.user)
            else:
                book.likes.remove(request.user)
            book.save()
        return redirect('index-page')


class OpenBook(View):
    def get(self, request, id, genre):
        comment = Comment.objects.filter(book_id=id)
        book = Books.objects.filter(id=id).annotate(com=Count('comment'))
        context = {'books': book,
                   'comment': comment,
                   }
        return render(request, 'manager/book.html', context=context)
