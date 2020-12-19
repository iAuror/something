from django.contrib.auth import login, logout
from django.db.models import Count, Avg, Q
from django.shortcuts import render, redirect
from django.views import View
from manager.forms import CommentForm
from manager.models import Books, Comment, BookRating, CommentLikes, Genre
from django.contrib.auth.forms import AuthenticationForm


class Shop(View):
    def get(self, request):
        books = Books.objects.prefetch_related('shop', 'genre',
                                               'author')  # .annotate(avg_rate=Avg('user_rate__rate')) (Аннтотация -Добавление поля в sql таблицу)
        books = books.annotate(count=Count('comment', distinct=True))
        genre = Genre.objects.all()
        comments = Comment.objects.all()

        context = {'title': 'Shop Book',
                   'books': books,
                   'comments': comments,
                   'range': range(1, 6),
                   'genre': genre,

                   }
        return render(request, 'manager/index.html', context=context)


class OpenBook(View):
    def get(self, request, slug):
        comment = Comment.objects.filter(book__slug=slug)
        book = Books.objects.filter(slug=slug).annotate(com=Count('comment'))
        # book = book.annotate(avg_rate=Avg('user_rate__rate'))

        context = {'books': book,
                   'comment': comment,
                   'range': range(1, 6),

                   }
        return render(request, 'manager/book.html', context=context)


class AddCommentLike(View):
    def get(self, request, id, slug):
        if request.user.is_authenticated:
            CommentLikes.objects.create(user=request.user, comment_id=id)
        return redirect('open-comment', slug=slug)


class OpenComment(View):
    def get(self, request, slug, ):
        comment = Comment.objects.filter(book__slug=slug)
        book = Books.objects.filter(slug=slug)
        genre=Genre.objects.all()

        context = {
            'genre':genre,
            'books': book,
            'form': CommentForm(),
            'comment': comment,

        }
        return render(request, 'manager/book_comment.html', context=context)


class AddBookRating(View):
    def get(self, request, id, rating, location=None):
        if request.user.is_authenticated:
            book_slug = Books.objects.get(id=id).slug
            BookRating.objects.create(user=request.user, book_id=id, rate=rating)
        if location is None:
            return redirect('index-page')
        else:
            return redirect('open-book', slug=book_slug)


class AddComment(View):
    def post(self, request, slug, book_id):
        if request.user.is_authenticated:
            com = CommentForm(data=request.POST)
            comment = com.save(commit=False)
            comment.book_id = book_id
            comment.save()
            # com.save_m2m ()
            comment.author_comment.add(request.user)
            CommentLikes.objects.get(user=request.user, comment_id=comment.id).delete()
            comment.save()

            return redirect('open-comment', slug=slug)

class Login(View):
    def post(self,request):
        user=AuthenticationForm(data=request.POST)
        if user.is_valid():
            login(request,user.get_user())
        return redirect('index-page')

    def get(self,request):
        context = {'form': AuthenticationForm()}
        return render(request, 'manager/login.html', context=context)

class Logout(View):
    def get(self,request):
        logout(request)
        return redirect('index-page')