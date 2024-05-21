from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, FormView
from .forms import DishesForm, PlaceForm, DishesPlaceForm, CategoryForm, PlaceInfo
from .models import Dishes, Category, Place
from django.contrib.auth.mixins import LoginRequiredMixin


#техническое меню
class HomeDish(ListView):  #(LoginRequiredMixin, ListView):
    model = Dishes

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная сраница'
        return context

    def get_queryset(self):
        return Dishes.objects.filter(is_public=True)

#пользовательское меню
class DishesByPlace(ListView):
    model = Dishes
    template_name = 'dishlist/index_menu.html'

    def get_queryset(self):
        return Dishes.objects.filter(place_id=self.kwargs['place_id'],
                                     is_public=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Place.objects.get(pk=self.kwargs['place_id'])

        context['active_var'] = 'Cкидка 10% на все меню'  # тестовое задание

        #отображение через сессию
        if 'active_var' not in self.request.session:
            self.request.session['active_var'] = 'Variable is now active for this session'
        context['active_var'] = self.request.session.get('active_var', None)

        return context

#отображение блюда пользователю
class ViewDishUser(DetailView):
    model = Dishes
    template_name = 'dishlist/dishes_detail_view.html'
    # pk_url_kwarg = "dishes_id"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        # Если вы хотите добавить название заведения:
        # context['title'] = Place.objects.get(pk=self.kwargs['place_id']).name
        return context




#главное меню редактора
class DashboardMenu(LoginRequiredMixin, ListView):
    model = Dishes
    template_name = 'dishlist/dashboard/index.html'

    def get_queryset(self):
        return Dishes.objects.filter(place_id=self.kwargs['place_id'], is_public=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        place = Place.objects.get(pk=self.kwargs['place_id'])
        context['title'] = place.title_place
        context['place_id'] = self.kwargs['place_id']

        # # Добавление названия плашки в контекст, если оно есть
        # if place.label:
        #     context['label_title'] = place.label.title
        # else:
        #     context['label_title'] = None

        return context


class DishesByPlaceAndCategorys(ListView):
    model = Dishes

    def get_queryset(self):
        return Dishes.objects.filter(place_id=self.kwargs['place_id'],
                                     category_id=self.kwargs['category_id'],
                                     is_public=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Place.objects.get(pk=self.kwargs['place_id'])
        return context

#отображение одного блюда в дашборде
class ViewDish(LoginRequiredMixin, DetailView):
    model = Dishes
    template_name = 'dishlist/dashboard/dishes_detail.html'
    #pk_url_kwarg = "dishes_id"

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        #context['title'] = Place.objects.get(pk=self.kwargs['place_id'])
        return context

class DishesByCategorys(ListView):
    model = Dishes
    #allow_empty = False  #запрещаем показ пустых страниц

    def get_queryset(self):
        return Dishes.objects.filter(category_id=self.kwargs['category_id'],
                                     is_public=True)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Category.objects.get(pk=self.kwargs['category_id'])
        return context

#страница редактирования категорий
class RefacrotCategory(LoginRequiredMixin, ListView):
    model = Category
    template_name = 'dishlist/dashboard/refactor_category.html'
    def get_queryset(self):
        # return Dishes.objects.filter(place_id=self.kwargs['place_id'],
        #                              is_public=True)
        return Category.objects.filter(place_id=self.kwargs['place_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Place.objects.get(pk=self.kwargs['place_id'])
        context['place_id'] = self.kwargs['place_id']
        return context




#редактирование категории
class UpdateCategory(LoginRequiredMixin, UpdateView):
    model = Category
    fields = ['title']
    template_name = 'dishlist/dashboard/update_category.html'

    def get_success_url(self):
        place_id = self.kwargs['place_id']
        return reverse_lazy('refactor_category', kwargs={'place_id': place_id})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Place.objects.get(pk=self.kwargs['place_id'])
        context['place_id'] = self.kwargs['place_id']
        return context

#редактирование блюд
class UpdateDishes(LoginRequiredMixin, UpdateView):
    model = Dishes
    form_class = DishesPlaceForm  # Используйте вашу кастомную форму
    template_name = 'dishlist/dashboard/update_dishes.html'

    def get_success_url(self):
        place_id = self.kwargs['place_id']
        return reverse_lazy('dashboard_menu', kwargs={'place_id': place_id})

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Place.objects.get(pk=self.kwargs['place_id']).title_place  # Добавьте .name для получения названия
        context['place_id'] = self.kwargs['place_id']
        return context

    def get_form_kwargs(self):
        kwargs = super(UpdateDishes, self).get_form_kwargs()  # Исправьте на UpdateDishes
        kwargs['user'] = self.request.user  # Добавляем текущего пользователя в параметры формы
        if not self.request.user.is_authenticated:
            raise PermissionDenied  # Если пользователь не аутентифицирован, запретите доступ
        return kwargs




#удаление блюда
class DeleteDish(LoginRequiredMixin, DeleteView):
    model = Dishes
    template_name = 'dishlist/dashboard/delete_dish.html'

    def get_success_url(self):
        place_id = self.kwargs['place_id']
        return reverse_lazy('dashboard_menu', kwargs={'place_id': place_id})

#удаление категории
class DeleteCategory(LoginRequiredMixin, DeleteView):
    model = Category
    template_name = 'dishlist/dashboard/delete_category.html'

    def get_success_url(self):
        place_id = self.kwargs['place_id']
        return reverse_lazy('refactor_category', kwargs={'place_id': place_id})



#создание места
class CreatePlace(LoginRequiredMixin, CreateView):
    form_class = PlaceForm
    template_name = 'dishlist/dashboard/add_place.html'
    #login_url = '/users/login/'

    def form_valid(self, form):
        w = form.save(commit=False)
        w.author =self.request.user
        return super().form_valid(form)

    # def get_success_url(self):
    #     place_id = self.kwargs['place_id']
    #     return reverse_lazy('dashboard_menu', kwargs={'place_id': place_id})

#добавление блюд для конкретного места
class CreateDishPlace(LoginRequiredMixin, CreateView): #LoginRequiredMixin, написать первым параметром
    form_class = DishesPlaceForm
    template_name = 'dishlist/dashboard/add_dishes.html'
    #login_url = '/users/login/'                 #параметры ограничения доступа
    #redirect_field_name = 'redirect_to'
    place = ["private_field"]

    def form_valid(self, form):
        w = form.save(commit=False)
        place_id = Place.objects.values('pk').get(author=self.request.user)
        w.place_id = place_id['pk']
        w.author = self.request.user
        return super().form_valid(form)

    def get_success_url(self, **kwargs):
        place_id = Place.objects.values('pk').get(author=self.request.user)
        place_id = place_id['pk']
        return reverse_lazy('dashboard_menu', args=[place_id])

    def get_form_kwargs(self):
        kwargs = super(CreateDishPlace, self).get_form_kwargs()
        kwargs['user'] = self.request.user  # Добавляем текущего пользователя в параметры формы
        return kwargs

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        place_id = Place.objects.values('pk').get(author=self.request.user)
        place_id = place_id['pk']
        title_place = Place.objects.values('title_place').get(author=self.request.user)  # Добавьте .name для получения названия
        context['title'] = title_place['title_place']
        context['place_id'] = place_id
        return context

class CreateCategory(LoginRequiredMixin, CreateView):
    form_class = CategoryForm
    template_name = 'dishlist/dashboard/add_category.html'

    def form_valid(self, form):
        w = form.save(commit=False)
        place_id = Place.objects.values('pk').get(author=self.request.user)
        w.place_id = place_id['pk']
        return super().form_valid(form)

    def get_success_url(self):
        place_id = Place.objects.values('pk').get(author=self.request.user)
        place_id = place_id['pk']
        return reverse_lazy('refactor_category', args=[place_id])




class PlaceInfoUpdateView(UpdateView):
    model = PlaceInfo
    fields = ['organization_name', 'inn', 'city', 'address', 'number_of_tables', 'working_hours', 'average_check']
    template_name = 'dishlist/dashboard/update_place_info.html'  # Замените на имя вашего шаблона
    success_url = reverse_lazy('update_place_info')  # Замените на имя вашего URL-адреса успешного обновления

    def get_object(self, queryset=None):
        # Получаем объект PlaceInfo, который хотим обновить
        return PlaceInfo.objects.get(place__author=self.request.user)

    def get_success_url(self):
        place_id = Place.objects.values('pk').get(author=self.request.user)
        place_id = place_id['pk']
        return reverse_lazy('update_place_info', args=[place_id])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = Place.objects.get(pk=self.kwargs['place_id']).title_place  # Добавьте .name для получения названия
        context['place_id'] = self.kwargs['place_id']
        return context

