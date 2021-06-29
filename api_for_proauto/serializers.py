from rest_framework.serializers import ModelSerializer
from proauto.models import Brend, Country, Auto


class BrendListSerializer(ModelSerializer):
    class Meta:
        model = Brend
        fields = ('title',  'slug', 'content')


class CountrySerializer(ModelSerializer):
    class Meta:
        model = Country
        fields = ('title', 'slug', 'content', 'cat')


class AutoSerializer(ModelSerializer):
    class Meta:
        model = Auto
        fields = ('title', 'slug', 'content', 'cat')




