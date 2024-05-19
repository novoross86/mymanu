from django.contrib import admin

from .models import Dishes, Category, Place

class DishesAdmin(admin.ModelAdmin):
    list_display = ('id', 'title',  'category', 'place', 'price', 'is_public')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'price')


admin.site.register(Dishes, DishesAdmin)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title')
    list_display_links = ('id', 'title')

admin.site.register(Category, CategoryAdmin)

class PlaceAdmin(admin.ModelAdmin):
    list_display = ('id', 'title_place')
    list_display_links = ('id', 'title_place')

admin.site.register(Place, PlaceAdmin)