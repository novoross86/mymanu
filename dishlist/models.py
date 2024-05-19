from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

#Плашка блюда
# class DisheLable(models.Model):
#     lable = models.ForeignKey('Lable', on_delete=models.PROTECT, blank=True, verbose_name="Текст плашки")
#     active = models.BooleanField(default=False)
#
# class Lable(models.Model):
#     title = models.CharField(max_length=50, db_index=True, verbose_name='Текст плашки')



class Dishes(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название')
    content = models.TextField(blank=True)
    photo = models.ImageField(blank=True, upload_to='photos/%Y/%m/%d/')
    price = models.DecimalField(max_digits=6, decimal_places=2, blank=True, verbose_name='Цена')
    is_public = models.BooleanField(default=True)
    update_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey('Category', on_delete=models.PROTECT, verbose_name="Категория")
    place = models.ForeignKey('Place', on_delete=models.PROTECT, verbose_name="Заведение")
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='dish_author', null=True, default=None)
    # маркет логика
    #dishe_lable = models.ForeignKey('DisheLable', on_delete=models.PROTECT, blank=True, verbose_name="Плашка")

    def get_absolute_url(self):
        return reverse('view_dishes', kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'
        ordering = ['category']


class Category(models.Model):
    title = models.CharField(max_length=150, db_index=True, verbose_name='Категории')
    place = models.ForeignKey('Place', on_delete=models.PROTECT, null=True, default=None,
                              verbose_name="Заведение")

    def get_absolute_url(self):
        return reverse('category', kwargs={"category_id": self.pk})

    def __str__(self):
        return self.title

    class Mete:
        verbose_name = 'Категории'
        verbose_name_plural = 'Категория'
        ordering = ['title']

#плашка для места

class PlaceLabel(models.Model):
    title = models.CharField(max_length=50, db_index=True, blank=True, verbose_name='Текст плашки')

    def __str__(self):
        return self.title

class Place(models.Model):
    title_place = models.CharField(max_length=150, db_index=True, verbose_name='Заведение')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='place_author', null=True,
                               default=None)
    label = models.ForeignKey('PlaceLabel', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Плашка")


# class Place(models.Model):
#     title_place = models.CharField(max_length=150, db_index=True, verbose_name='Заведение')
#     author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='place_author', null=True,
#                                default=None)
#     lable = models.ManyToManyField(PlaceLabel, blank=True)

    def get_absolute_url(self):
        return reverse('dashboard_menu', kwargs={"place_id": self.pk})

    def __str__(self):
        return self.title_place

    class Mete:
        verbose_name = 'Заведение'
        verbose_name_plural = 'Заведения'
        ordering = ['title_place']

#раздел маркет моделей





