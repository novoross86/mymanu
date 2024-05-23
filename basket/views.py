from django.contrib.sessions.models import Session
from django.shortcuts import render, redirect, get_object_or_404
from dishlist.models import Dishes
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import BasketItem


def dish_list(request):
    dishes = Dishes.objects.all()
    print(dishes)
    return render(request, 'basket/dish.html', {'dishes': dishes})


def view_basket(request):
    # Получаем все элементы корзины для текущей сессии
    basket_items = BasketItem.objects.filter(session=request.session.session_key)

    # Если в корзине нет товаров, устанавливаем место и id места в None
    place = None
    place_id = None

    # Если в корзине есть товары, получаем место из первого товара
    if basket_items:
        place = basket_items[0].dishe.place
        place_id = basket_items[0].dishe.place_id

    # Рассчитываем общую стоимость товаров в корзине
    total_price = sum(item.dishe.price * item.quantity for item in basket_items)

    # Отправляем данные в шаблон
    return render(request, 'basket/basket1.html', {
        'basket_items': basket_items,
        'total_price': total_price,
        'place': place,
        'place_id': place_id
    })


# def add_to_basket(request, dish_id):
#     dish = get_object_or_404(Dishes, id=dish_id)
#     session_key = request.session.session_key
#     if not session_key:
#         request.session.create()
#         session_key = request.session.session_key
#     session = Session.objects.get(session_key=session_key)
#
#     basket_item, created = BasketItem.objects.get_or_create(
#         dishe=dish,
#         session=session,
#         defaults={'quantity': 0}  # Установка начального количества, если создается новый объект
#     )
#     basket_item.quantity += 1
#     basket_item.save()
#
#     #return redirect('place', dish.place_id)
#     return JsonResponse({'quantity': basket_item.quantity})

def add_to_basket(request, dish_id):
    dish = get_object_or_404(Dishes, id=dish_id)

    session_key = request.session.session_key
    if not session_key:
        request.session.create()
        request.session.save()
        session_key = request.session.session_key
    session = Session.objects.get(session_key=session_key)

    # Установка цены за единицу товара
    price_per_item = dish.price

    basket_item, created = BasketItem.objects.get_or_create(
        dishe=dish,
        session=session,
        defaults={'quantity': 1, 'price_per_item': price_per_item}  # Установка начального количества и цены
    )
    if not created:
        basket_item.quantity += 1
        basket_item.save()

    return JsonResponse({'quantity': basket_item.quantity})

#save orders
@csrf_exempt
def save_order_data(request):
    if request.method == 'POST':
        # Обработка данных заказа и их сохранение
        return JsonResponse({'status': 'success'})
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request'}, status=400)





def remove_from_basket(request, item_id):
    basket_item = BasketItem.objects.get(id=item_id)
    if basket_item.quantity > 1:
        basket_item.quantity -= 1
        basket_item.save()
    else:
        basket_item.delete()
    return redirect('view_basket')



@require_POST
def save_basket(request):
    # Здесь ваш код для сохранения данных корзины
    session_key = request.POST.get('session_key')
    basket_items = BasketItem.objects.filter(session__session_key=session_key)
    # ... сохранение данных заказа ...
    return JsonResponse({'status': 'success'})
