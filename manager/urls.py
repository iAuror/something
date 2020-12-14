from django.urls import path, include

from manager.views import Shop, OpenBook, OpenComment, AddCommentLike, AddBookRating

urlpatterns = [
    path('', Shop.as_view(), name='index-page'),

    path('book/<int:id>/', OpenBook.as_view(), name='open-book'),
    path('commentary/<int:id>/', AddCommentLike.as_view(), name='add-comment-like'),
    path('commentary/<str:title>/<int:id>/', OpenComment.as_view(), name='open-comment'),
    path('add-rating/<int:id>/<int:rating>', AddBookRating.as_view(), name='add-rating'),
    path('add-rating/<int:id>/<int:rating>/<str:location>/', AddBookRating.as_view(), name='add-rating-location'),

]
