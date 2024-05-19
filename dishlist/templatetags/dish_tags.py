from django import template

from dishlist.models import Category, Place, Dishes

register = template.Library()

@register.simple_tag()
def get_categories():
    return Category.objects.all()

@register.inclusion_tag('dishlist/list_categories.html')
def show_categories():
    categories = Category.objects.all()
    return {"categories": categories}

@register.simple_tag()
def get_places():
    return Place.objects.all()


@register.inclusion_tag('dishlist/list_places.html')
def show_places():
    place = Place.objects.all()
    return {"place": place}
