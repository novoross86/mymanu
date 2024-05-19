# from django.utils import timezone
# from datetime import timedelta
# from django.conf import settings
# from django.contrib.sessions.models import Session
# import datetime
#
# from basket.views import save_basket_on_session_end
#
#
# class SessionIdleTimeoutMiddleware:
#     def __init__(self, get_response):
#         self.get_response = get_response
#
#     def __call__(self, request):
#         # Получаем текущую сессию
#         session_key = request.session.session_key
#         if session_key:
#             session = Session.objects.get(session_key=session_key)
#             # Проверяем время последнего действия
#             last_activity = session.get_decoded().get('last_activity')
#             if last_activity:
#                 last_activity_time = timezone.make_aware(datetime.datetime.strptime(last_activity, '%Y-%m-%d %H:%M:%S'))
#                 # Если с момента последнего действия прошло больше 60 минут
#                 if timezone.now() - last_activity_time > timedelta(minutes=60):
#                     # Здесь можно вызвать функцию для сохранения корзины
#                     save_basket_on_session_end(request)
#                     # И затем удаляем сессию
#                     session.delete()
#             # Обновляем время последнего действия
#             request.session['last_activity'] = timezone.now().strftime('%Y-%m-%d %H:%M:%S')
#         response = self.get_response(request)
#         return response
#
# # Не забудьте добавить ваш новый middleware в MIDDLEWARE в settings.py
