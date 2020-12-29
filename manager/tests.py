from django.contrib.auth.models import User
from django.test import TestCase, TransactionTestCase

# Create your tests here. coverage run --source='.' manage.py test
from django.urls import reverse
from slugify import slugify

from manager.models import Books, Pub_office, Genre, Comment


class ShopTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_user')
        self.user2 = User.objects.create_user('test_user2')
        Pub_office.objects.create(publisher='Mir knigi')
        Genre.objects.create(genre='romanse')

    def test_addbook(self):
        self.client.force_login(self.user)

        self.assertTrue(Pub_office.objects.exists(), msg='we have no publisher')
        url = reverse('add-book')
        data = {
            'title': 'test title name',
            'text': 'some text',
            'shop': '1',
            'genre': '1',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302, msg='book dont create')
        self.assertTrue(Books.objects.exists(), msg='we have no book')
        self.assertEqual(Books.objects.first().slug, slugify(data['title']), msg='slug error')
        book = Books.objects.first()
        self.assertEqual(book.author.first(), self.user, msg='User is not author')
        self.client.logout()
        data = {
            'title': 'test title name_new',
            'text': 'some text',
            'shop': '1',
            'genre': '1',
        }
        response = self.client.post(url, data)
        self.assertEqual(Books.objects.count(), 1, msg='create book without author')
        self.client.force_login(self.user)
        response = self.client.post(url, data)
        self.assertEqual(Books.objects.count(), 2, msg='problem with second book create')

    def test_update_book(self):
        self.client.force_login(self.user)

        self.assertTrue(Pub_office.objects.exists(), msg='we have no publisher')
        url = reverse('add-book')
        data = {
            'title': 'test title name',
            'text': 'some text',
            'shop': '1',
            'genre': '1',
        }
        response = self.client.post(url, data)
        self.assertTrue(Books.objects.exists(), msg='we have no book')
        data['title'] = 'test title new'
        self.slug = Books.objects.first().slug
        url = reverse('update-book', kwargs=dict(slug=self.slug))
        response = self.client.post(url, data, )
        self.assertEqual(Books.objects.count(), 1, msg='we have more 1 book')

        self.assertEqual(Books.objects.first().title, data['title'], msg='title dont update')
        self.client.logout()
        data['title'] = 'logout title'
        response = self.client.post(url, data, )
        self.assertNotEqual(Books.objects.first().title, data['title'], msg='title update logout user')

        self.client.force_login(self.user2)
        response = self.client.post(url, data, )
        self.assertNotEqual(Books.objects.first().title, data['title'], msg='title update another user')

    def test_delete_book(self):
        self.client.force_login(self.user)

        self.assertTrue(Pub_office.objects.exists(), msg='we have no publisher')
        url = reverse('add-book')
        data = {
            'title': 'test title name',
            'text': 'some text',
            'shop': '1',
            'genre': '1',
        }
        response = self.client.post(url, data)
        self.slug = Books.objects.first().slug
        url = reverse('delete-book', kwargs=dict(slug=self.slug))
        self.client.logout()
        response = self.client.post(url, data)
        self.assertTrue(Books.objects.exists(), msg='delete book when logout')
        self.client.force_login(self.user2)
        response = self.client.post(url, data)
        self.assertTrue(Books.objects.exists(), msg='another author delete book')
        self.client.logout()
        self.client.force_login(self.user)
        response = self.client.post(url, data)
        self.assertEqual(Books.objects.count(), 0, msg='user cant delete book')

    def test_rate(self):
        self.client.force_login(self.user)
        self.book1 = Books.objects.create(title='test', text='test text', shop_id='1', genre_id='1')
        self.book1.author.add(self.user)
        self.book1.save()
        url = reverse('add-rating', kwargs=dict(slug=self.book1.slug, rating=4))
        self.client.get(url)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.rate, 4, msg='first rate trouble')
        self.client.force_login(self.user2)
        url = reverse('add-rating', kwargs=dict(slug=self.book1.slug, rating=1))
        self.client.get(url)
        self.book1.refresh_from_db()
        self.assertEqual(self.book1.rate, 2.5, msg='trouble with rerate')

    def test_add_comment(self):
        self.client.force_login(self.user)
        self.book1 = Books.objects.create(title='test', text='test text', shop_id='1', genre_id='1')
        self.book1.author.add(self.user)
        self.book1.save()
        url = reverse('add-comment', kwargs=dict(slug=self.book1.slug))
        data = {
            'text': 'test comment',
        }
        self.client.post(url, data)
        self.assertTrue(Comment.objects.exists(), msg='comment dont create')
        self.assertEqual(Comment.objects.first().book_id, self.book1.slug, msg='comment dont root book')
        comment=Comment.objects.first()
        comment.author_comment.add(self.user)
        comment.save()

        data={
            'text':'new comment'
        }
        url=reverse('update-comment', kwargs=dict(slug=self.book1.slug, id=comment.id))
        self.client.post(url,data)
        comment.refresh_from_db()
        self.assertEqual(comment.text, data['text'], msg='comment dont update')
        self.client.logout()
        data = {
             'text': 'new comment-1'
         }
        url = reverse('update-comment', kwargs=dict(slug=self.book1.slug, id=comment.id))
        self.client.post(url, data)
        comment.refresh_from_db()
        self.assertNotEqual(comment.text, data['text'], msg='update comment with logout user')


    def test_add_like_to_comment(self):
        self.client.force_login(self.user)
        self.book1 = Books.objects.create(title='test', text='test text', shop_id='1', genre_id='1')

        self.comment = Comment.objects.create(book_id=self.book1.slug, text='test text')
        self.comment.author_comment.add(self.user)
        self.comment.save()
        # print(self.comment.id, self.book1.slug, self.comment.book)
        self.client.force_login(self.user2)
        url = reverse('add-comment-like', kwargs=dict(slug=self.book1.slug, id=self.comment.id))
        self.client.get(url)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.likes_count, 1, msg='comment have no like')
        self.client.logout()
        self.client.get(url)
        self.comment.refresh_from_db()
        self.assertEqual(self.comment.likes_count, 1, msg='comment like without user')

    def test_logout(self):
        self.client.force_login(self.user)
        url=reverse('logout')
        self.client.get(url)
        self.assertTrue(User.objects.first().is_active, msg='not logout')


class NewTest(TransactionTestCase):
    def setUp(self):
        self.user = User.objects.create_user('test_user')
        self.user2 = User.objects.create_user('test_user2')
        Pub_office.objects.create(publisher='Mir knigi')
        Genre.objects.create(genre='romanse')

    # def test_add_like_to_comment(self):
    # self.client.force_login(self.user)
    # self.book1 = Books.objects.create(title='test', text='test text', shop_id='1', genre_id='1')
    #
    # self.comment=Comment.objects.create(book_id=self.book1.slug, text='test text')
    # self.comment.author_comment.add(self.user)
    # self.comment.save()
    # print(self.comment.id, self.book1.slug, self.comment.book)
    # url=reverse('add-comment-like',kwargs=dict(slug=self.book1.slug, id=self.comment.id))
    # # self.client.get(url)
    # # self.client.get(url)
    # # self.comment.refresh_from_db()
    # # self.assertEqual(self.comment.likes_count, 0, msg='comment have no like')
    # self.client.force_login(self.user2)
    # self.client.get(url)
    # self.assertEqual(self.comment.likes_count, 1, msg='comment have no like')
