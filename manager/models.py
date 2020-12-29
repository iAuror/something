from django.contrib.auth.models import User
from django.db import models
from slugify import slugify


class Books(models.Model):
    title = models.CharField(max_length=100, verbose_name='Оглавление', )
    text = models.TextField(verbose_name='Текст книги')
    published = models.DateTimeField(auto_now_add=True, verbose_name='Время публикации')
    shop = models.ForeignKey('Pub_office', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, null=True, verbose_name='Жанр')
    author = models.ManyToManyField(User, related_name='books')
    rate = models.DecimalField(max_digits=3, decimal_places=2, verbose_name='Рейтинг', default=0.0)
    count_rate_users = models.PositiveIntegerField(default=0)
    rate_all_stars = models.PositiveIntegerField(default=0)
    ratting = models.ManyToManyField(User, related_name='book_rating', through='manager.BookRating')
    slug = models.SlugField(primary_key=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title

    def save(self, **kwargs):
        if self.slug == '':
            self.slug = slugify(self.title)
        try:
            super().save(**kwargs)
        except:
            self.slug += str(self.published)
            super().save(**kwargs)


class BookRating(models.Model):
    class Meta:
        unique_together = ('book', 'user')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='book_rate')
    rate = models.SmallIntegerField(verbose_name='Суммарный рейтинг', default=0)
    book = models.ForeignKey(Books, on_delete=models.CASCADE, related_name='user_rate', null=True)

    def save(self, **kwargs):
        try:
            super().save(**kwargs)
        except:
            br = BookRating.objects.get(user=self.user, book=self.book, )
            self.book.rate_all_stars -= br.rate
            br.rate = self.rate
            br.save()
        else:
            self.book.count_rate_users += 1
        self.book.rate_all_stars += self.rate
        self.book.rate = self.book.rate_all_stars / self.book.count_rate_users
        self.book.save()


class Pub_office(models.Model):
    publisher = models.CharField(max_length=100, verbose_name='Издатель', )

    def __str__(self):
        return self.publisher

    class Meta:
        verbose_name = 'Издательства'
        verbose_name_plural = 'Издательства'


class Genre(models.Model):
    genre = models.CharField(max_length=100, verbose_name='Жанр')

    def __str__(self):
        return self.genre

    class Meta:
        verbose_name = 'Жанр '
        verbose_name_plural = 'Жанры'


class Comment(models.Model):
    book = models.ForeignKey('Books', on_delete=models.CASCADE, related_name='comment', null=True)
    text = models.TextField(verbose_name='Комментарий')
    comment_date = models.DateTimeField(auto_now_add=True)
    author_comment = models.ManyToManyField(User, related_name='comment_likers', through='CommentLikes')
    likes_count = models.IntegerField(default=0)

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text


class CommentLikes(models.Model):
    class Meta:
        unique_together = ('comment', 'user')

    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comment_like')

    def save(self, **kwargs):
        try:
            super().save(**kwargs)
        except:
            CommentLikes.objects.get(user=self.user, comment=self.comment).delete()
            self.comment.likes_count -= 1
        else:
            self.comment.likes_count += 1
        self.comment.save()
