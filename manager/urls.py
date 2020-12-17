from django.urls import path, include

from manager.views import Shop, OpenBook, OpenComment, AddCommentLike, AddBookRating, AddComment, Login, Logout

urlpatterns = [
    path('', Shop.as_view(), name='index-page'),

    path('book/<str:slug>/', OpenBook.as_view(), name='open-book'),
    path('commentary/<str:slug>/<int:id>/', AddCommentLike.as_view(), name='add-comment-like'),
    path('commentary/<str:slug>/', OpenComment.as_view(), name='open-comment'),
    path('add-rating/<int:id>/<int:rating>', AddBookRating.as_view(), name='add-rating'),
    path('add-rating/<int:id>/<int:rating>/<str:location>/', AddBookRating.as_view(),
         name='add-rating-location'),
    path('<str:slug>/add-comment/<int:book_id>', AddComment.as_view(), name='add-comment'),
    path('login/' , Login.as_view(), name='login'),
    path('logout/' , Logout.as_view(), name='logout'),
]
