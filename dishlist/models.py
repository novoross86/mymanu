from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse
from django.dispatch import receiver
from django.db.models.signals import post_save


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

# class PlaceLabel(models.Model):
#     title = models.CharField(max_length=50, db_index=True, blank=True, verbose_name='Текст плашки')
#
#     def __str__(self):
#         return self.title

# class Place(models.Model):
#     title_place = models.CharField(max_length=150, db_index=True, verbose_name='Заведение')
#     author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='place_author', null=True,
#                                default=None)
#     # label = models.ForeignKey('PlaceLabel', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Плашка")
#     place_info = models.OneToOneField('PlaceInfo', on_delete=models.SET_NULL, null=True, blank=True)
#
#     def get_absolute_url(self):
#         return reverse('dashboard_menu', kwargs={"place_id": self.pk})
#
#     def __str__(self):
#         return self.title_place
#
#     class Mete:
#         verbose_name = 'Заведение'
#         verbose_name_plural = 'Заведения'
#         ordering = ['title_place']


class Place(models.Model):
    title_place = models.CharField(max_length=150, db_index=True, verbose_name='Заведение')
    author = models.ForeignKey(get_user_model(), on_delete=models.SET_NULL, related_name='place_author', null=True,
                               default=None)
    # label = models.ForeignKey('PlaceLabel', on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Плашка")
    place_info = models.OneToOneField('PlaceInfo', on_delete=models.SET_NULL, null=True, blank=True, related_name='place_info_reverse')

    def get_absolute_url(self):
        return reverse('dashboard_menu', kwargs={"place_id": self.pk})

    def __str__(self):
        return self.title_place

    class Meta:
        verbose_name = 'Заведение'
        verbose_name_plural = 'Заведения'
        ordering = ['title_place']

# модель информации о заведении
class PlaceInfo(models.Model):
    place = models.ForeignKey(Place, related_name='info_set', on_delete=models.CASCADE, verbose_name='Заведение')
    organization_name = models.CharField(max_length=255, null=True, verbose_name='Название организации')
    inn = models.PositiveIntegerField(verbose_name='ИНН',null=True, unique=True)
    city = models.CharField(max_length=100, null=True, verbose_name='Город')
    address = models.CharField(max_length=255, null=True, verbose_name='Адрес')
    number_of_tables = models.PositiveIntegerField(null=True, verbose_name='Количество столиков')
    working_hours = models.CharField(max_length=255, null=True, verbose_name='Часы работы')
    average_check = models.PositiveIntegerField(null=True, verbose_name='Средний чек')

    def __str__(self):
        return f"{self.organization_name} ({self.place.title_place})"

    class Meta:
        verbose_name = 'Информация о заведении'
        verbose_name_plural = 'Информация о заведениях'


    @receiver(post_save, sender=Place)
    def create_place_info(sender, instance, created, **kwargs):
        if created:
            PlaceInfo.objects.create(place=instance)



