from django import forms
from .models import Dishes, Place, Category, PlaceInfo


#добавление блюда
class DishesPlaceForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super(DishesPlaceForm, self).__init__(*args, **kwargs)
        if user and user.is_authenticated:
            # Получаем список id заведений, которые принадлежат пользователю
            user_places = Place.objects.filter(author=user).values_list('id', flat=True)
            # Фильтруем категории по списку id заведений
            self.fields['category'].queryset = Category.objects.filter(place_id__in=user_places)

    class Meta:
        model = Dishes
        fields = ['title', 'content', 'price', 'is_public', 'category', 'photo']

#добавление организации
class PlaceForm(forms.ModelForm):
    class Meta:
        model = Place
        fields = ['title_place']

#добавление категории
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['title']

#добавление блюд старое но чтото от него зависит
class DishesForm(forms.ModelForm):
    class Meta:
        model = Dishes
        fields = ['title', 'content', 'price', 'is_public', 'place', 'category', 'photo']


class PlaceInfoForm(forms.ModelForm):
    class Meta:
        model = PlaceInfo
        fields = '__all__'  # Все поля модели PlaceInfo