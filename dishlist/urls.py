from django.urls import path
from . import views

urlpatterns = [
    #техническое меню
    path('', views.HomeDish.as_view(), name='home'),
    #пользовательское меню
    path('place/<int:place_id>/', views.DishesByPlace.as_view(), name='place'),
    #отображение одного блюда пользователю
    path('dishes_user/<int:pk>/', views.ViewDishUser.as_view(), name='view_dishes_user'),
    path('category/<int:category_id>/', views.DishesByCategorys.as_view(), name='category'),
    path('place_cat/<int:place_id>/<int:category_id>/', views.DishesByPlaceAndCategorys.as_view, name='place_cat'),

    #отображение одного блюда в дашборде
    path('dishes/<int:pk>/', views.ViewDish.as_view(), name='view_dishes'),
    path('add_place/', views.CreatePlace.as_view(), name='add_place'),
    #главное меню редактора
    path('dashboard_menu/<int:place_id>/', views.DashboardMenu.as_view(), name='dashboard_menu'),
    path('add_dishes_place/', views.CreateDishPlace.as_view(), name='add_dishes_place'),
    #создание категории
    path('add_category/', views.CreateCategory.as_view(), name='add_category'),
    #редактирование категорий
    path('refactor_category/<int:place_id>/', views.RefacrotCategory.as_view(), name='refactor_category'),
    #изменение категории
    path('update_category/<int:place_id>/<int:pk>', views.UpdateCategory.as_view(), name='update_category'),
    #удаление категории
    path('delete_category/<int:place_id>/<int:pk>/', views.DeleteCategory.as_view(), name='delete_category'),
    #изменение блюд
    path('update_dishes/<int:place_id>/<int:pk>', views.UpdateDishes.as_view(), name='update_dishes'),
    #удаление блюда
    path('delete_dish/<int:place_id>/<int:pk>/', views.DeleteDish.as_view(), name='delete_dish'),
    #редактирование данных организации
    path('place_info/<int:place_id>/', views.PlaceInfoUpdateView.as_view(), name='update_place_info'),

]