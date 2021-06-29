from django.urls import path, include
from .views import TelegramView, index
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', index, name='index'),
    path('bot/', csrf_exempt(TelegramView.as_view())),

            ]