from django.urls import path, include
from django.views.decorators.cache import cache_page
from manager.views import Shop, OpenBook, OpenComment, AddCommentLike, AddBookRating, \
    AddComment, Login, Logout, AddBook, delete_book, UpdateBook, UpdateComment, CreateUser

urlpatterns = [
    #path('', Shop.as_view(), name='index-page'),
    path('', cache_page(5)(Shop.as_view()), name='index-page'),
    path('book/<str:slug>/', OpenBook.as_view(), name='open-book'),
    path('commentary/<str:slug>/<int:id>/', AddCommentLike.as_view(), name='add-comment-like'),
    path('commentary/<str:slug>/', OpenComment.as_view(), name='open-comment'),
    path('add-rating/<str:slug>/<int:rating>', AddBookRating.as_view(), name='add-rating'),
    path('add-rating/<str:slug>/<int:rating>/<str:location>/', AddBookRating.as_view(),
         name='add-rating-location'),
    path('<str:slug>/add-comment/', AddComment.as_view(), name='add-comment'),
    path('login/' , Login.as_view(), name='login'),
    path('register/', CreateUser.as_view(), name='register'),
    path('logout/' , Logout.as_view(), name='logout'),
    path('add-book/',AddBook.as_view(), name='add-book' ),
    path('delete-book/<str:slug>/', delete_book, name='delete-book'),
    path('update-book/<str:slug>/', UpdateBook.as_view(), name='update-book'),
    path('update-comment/<str:slug>/<int:id>',UpdateComment.as_view(),name='update-comment'),
]
