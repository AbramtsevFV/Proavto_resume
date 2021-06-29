from django.urls import path, include
from .views import *

urlpatterns = [
    path('', HomePage.as_view(), name='glavnaya'),
    path('brend/<slug:brend_slug>', Brend_auto.as_view(), name='brend'),
    path('country/<slug:country_slug>', Country.as_view(), name='country'),
    path('car_model/<slug:auto_slug>', Car_model.as_view(), name='auto'),
    path('search/', SearchCar.as_view(), name='search'),
    path('feedback_page/', Feedback.as_view(), name='feedback'),

]

