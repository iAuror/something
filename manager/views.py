from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from manager.models import Books


def buy(request):
    return HttpResponse('<h1>Временная заглушка</h1>')


class Shop(View):
    def get(self, request):
        books = Books.objects.all()
        context = {'title': 'Shop Book',
                   'name': ['Egor', 'Oleg', 'Anton'],
                   'books': books
                   }
        return render(request, 'manager/index.html', context=context)
