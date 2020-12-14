from django.db.models import Count, Avg, Q
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View

from manager.models import Books, Comment, BookRating, CommentLikes, Genre


class Shop(View):
    def get(self, request):
        books = Books.objects.prefetch_related('shop', 'genre','author' )  #.annotate(avg_rate=Avg('user_rate__rate')) (Аннтотация -Добавление поля в sql таблицу)
        books = books.annotate(count=Count('comment', distinct=True))
        genre=Genre.objects.all()
        comments = Comment.objects.all()

        context = {'title': 'Shop Book',
                   'books': books,
                   'comments': comments,
                   'range': range(1, 6),
                   'genre': genre,

                   }
        return render(request, 'manager/index.html', context=context)




class OpenBook(View):
    def get(self, request, id, ):
        comment = Comment.objects.filter(book_id=id)
        book = Books.objects.filter(id=id).annotate(com=Count('comment'))
        #book = book.annotate(avg_rate=Avg('user_rate__rate'))

        context = {'books': book,
                   'comment': comment,
                   'range': range(1, 6),

                   }
        return render(request, 'manager/book.html', context=context)


class AddCommentLike(View):
    def get(self, request, id):
        if request.user.is_authenticated:
            CommentLikes.objects.create(user=request.user, comment_id=id)
        return redirect('index-page')


class OpenComment(View):
    def get(self, request, id, title):
        comment = Comment.objects.filter(book_id=id).prefetch_related('name')
        book = Books.objects.filter(id=id)

        context = {
            'books': book,

            'comment': comment,

        }
        return render(request, 'manager/book_comment.html', context=context)


class AddBookRating(View):
    def get(self, request, id, rating, location=None):
        if request.user.is_authenticated:
            BookRating.objects.create(user=request.user, book_id=id, rate=rating)
        if location is None:
            return redirect('index-page')
        else:
            return redirect('open-book', id=id)