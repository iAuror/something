from django.db import models


class Books(models.Model):
    title = models.CharField(max_length=100, verbose_name='Оглавление', )
    text = models.TextField(verbose_name='Текст книги')
    published = models.DateTimeField(auto_now_add=True, verbose_name='Время публикации')
    shop = models.ForeignKey('Pub_office', on_delete=models.CASCADE)
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'

    def __str__(self):
        return self.title


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