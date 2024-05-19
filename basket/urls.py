from django.urls import path
from basket.views import dish_list, add_to_basket, remove_from_basket, view_basket, save_order_data
from . import views


urlpatterns = [
	path('dish/', dish_list, name='dish_list'),
	path('basket/', view_basket, name='view_basket'),
	path('add_to_basket/<int:dish_id>/', add_to_basket, name='add_to_basket'),
	path('remove_from_basket/<int:item_id>/', remove_from_basket, name='remove_from_basket'),
	path('save_order/', save_order_data, name='save_order_data'),
]
