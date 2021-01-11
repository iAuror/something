from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.db.models import Count, Avg, Q, OuterRef, Exists
from django.shortcuts import render, redirect
from django.views import View
from manager.forms import CommentForm, BooksForm, CustomUserCreationForm, CustomAuthenticationForm
from manager.models import Books, Comment, BookRating, CommentLikes, Genre
from django.contrib.auth.forms import AuthenticationForm
from django.views.decorators.cache import cache_page
from django.core.paginator import Paginator

class Shop(View):
    def get(self, request):
        books = Books.objects.prefetch_related('shop', 'genre',
                                               'author')  # .annotate(avg_rate=Avg('user_rate__rate')) (Аннтотация -Добавление поля в sql таблицу)
        books = books.annotate(count=Count('comment', distinct=True))
        genre = Genre.objects.all()
        comments = Comment.objects.all()
        if request.user.is_authenticated:
            is_owner = Exists(User.objects.filter(books=OuterRef('pk'), id=request.user.id))
            books = books.annotate(is_owner=is_owner)
        paginator=Paginator (books , 4)
        context = {'title': 'Shop Book',
                   'books': paginator.get_page(request.GET.get('page',1)),
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
        genre = Genre.objects.all()
        context = {'book': book,
                   'comment': comment,
                   'range': range(1, 6),
                   'genre': genre
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
        genre = Genre.objects.all()
        if request.user.is_authenticated:
            is_owner = Exists(User.objects.filter(comment_likers=OuterRef('pk'), id=request.user.id))
            comment = comment.annotate(is_owner=is_owner)

        context = {
            'genre': genre,
            'books': book,
            'form': CommentForm(),
            'comment': comment,

        }
        return render(request, 'manager/book_comment.html', context=context)


class AddBookRating(View):
    def get(self, request, slug, rating, location=None):
        if request.user.is_authenticated:
            BookRating.objects.create(user=request.user, book_id=slug, rate=rating)
        if location is None:
            return redirect('index-page')
        else:
            return redirect('open-book', slug=slug)


class AddComment(View):
    def post(self, request, slug, ):
        if request.user.is_authenticated:
            com = CommentForm(data=request.POST)
            comment = com.save(commit=False)
            comment.book_id = slug
            comment.save()
            # com.save_m2m ()
            comment.author_comment.add(request.user)
            CommentLikes.objects.get(user=request.user, comment_id=comment.id).delete()
            comment.save()

            return redirect('open-comment', slug=slug)


class CreateUser(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'manager/register.html', {'form': form})

    def post(self, request):
        user = CustomUserCreationForm(data=request.POST)
        if user.is_valid():
            user.save()
            return redirect('login')
        else:
            messages.error(request, user.error_messages)
            return redirect('register')


class Login(View):
    def post(self, request):
        user = CustomAuthenticationForm(data=request.POST)
        if user.is_valid():
            login(request, user.get_user())
            return redirect('index-page')
        messages.error(request, user.error_messages)
        return redirect('login')

    def get(self, request):
        context = {'form': CustomAuthenticationForm()}
        return render(request, 'manager/login.html', context=context)


class Logout(View):
    def get(self, request):
        logout(request)
        return redirect('index-page')


class AddBook(View):
    def get(self, request):
        book = Books.objects.all()
        context = {
            'books': book,
            'form': BooksForm()
        }
        return render(request, 'manager/add_book.html', context)

    def post(self, request):
        if request.user.is_authenticated:
            book = BooksForm(data=request.POST)
            if book.is_valid():
                add_book = book.save(commit=True)
                add_book.author.add(request.user)
                add_book.save()
        return redirect('index-page')


def delete_book(request, slug):
    if request.user.is_authenticated:
        book = Books.objects.get(slug=slug)
        if request.user in book.author.all():
            Books.objects.get(slug=slug).delete()
    return redirect('index-page')


class UpdateBook(View):
    def get(self, request, slug):
        if request.user.is_authenticated:
            book = Books.objects.get(slug=slug)
            if request.user in book.author.all():
                form = BooksForm(instance=book)
                slug = book.slug
                context = {
                    'form': form,
                    'slug': slug,
                }
                return render(request, 'manager/update_book.html', context=context)
        return redirect('index-page')

    def post(self, request, slug):
        if request.user.is_authenticated:
            book = Books.objects.get(slug=slug)
            if request.user in book.author.all():
                u_book = BooksForm(data=request.POST, instance=book)
                if u_book.is_valid():
                    u_book.save(commit=True)
        return redirect('index-page')


class UpdateComment(View):
    def get(self, request, slug, id):
        if request.user.is_authenticated:
            comment = Comment.objects.get(id=id)
            book = Books.objects.get(slug=slug)
            genre = Genre.objects.all()
            if request.user in comment.author_comment.all():
                form = CommentForm(instance=comment)
                context = {
                    'genre': genre,
                    'books': book,
                    'form': form,
                    'comment': comment,
                }
                return render(request, 'manager/update_comment.html', context=context)
        return redirect('index-page')

    def post(self, request, id, slug):
        if request.user.is_authenticated:
            comment = Comment.objects.get(id=id)
            if request.user in comment.author_comment.all():
                u_comment = CommentForm(data=request.POST, instance=comment)
                u_comment.save(commit=True)
                return redirect('open-comment', slug=slug)
        return redirect('index-page')
