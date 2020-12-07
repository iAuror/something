from django.urls import path, include

from manager.views import buy, Shop, AddLike, OpenBook

urlpatterns = [
    path('', Shop.as_view(), name='index-page'),
    path ('add-like/<int:id>/', AddLike.as_view(),name='add-like'),
    path ('book/<str:genre>/<int:id>',OpenBook.as_view(),name='open-book' ),

    #path('/add-like/<int:id>,'),
]
