from django.contrib import admin

from manager.models import Books, Pub_office, Genre


class BooksAdmin (admin.ModelAdmin):
    list_display = ('id','title','published','shop','genre')
    list_display_links = ('title',)

class Pub_officeAdmin (admin.ModelAdmin):
    list_display = ('id','publisher')

class GenreAdmin (admin.ModelAdmin):
    list_display = ('genre',)

admin.site.register(Books,BooksAdmin)
admin.site.register(Pub_office,Pub_officeAdmin)
admin.site.register(Genre,GenreAdmin)