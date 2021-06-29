from django.shortcuts import render
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.renderers import JSONRenderer
from .serializers import BrendListSerializer, CountrySerializer, AutoSerializer
from proauto.models import Brend, Country, Auto

class CountryViewSet(ModelViewSet):
    renderer_classes = [JSONRenderer]
    queryset = Country.objects.all()
    serializer_class = CountrySerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('slug',)

class BrendViewSet(ModelViewSet):
    """
    api/v1/brend/?search=VAZ
    Поиск происходит по slug
    """
    renderer_classes = [JSONRenderer]
    queryset = Brend.objects.all()
    serializer_class = BrendListSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('slug',)

class AutoViewSet(ModelViewSet):
    """
    api/v1/model_auto/?search=ВАЗ-2101
    поиск происходит по title
    """
    renderer_classes = [JSONRenderer]
    queryset = Auto.objects.all()
    serializer_class = AutoSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('title','slug')

