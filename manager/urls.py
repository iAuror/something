from django.urls import path

from manager.views import buy

urlpatterns = [
    path ('', buy)
]
