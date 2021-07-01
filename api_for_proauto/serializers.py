from rest_framework.serializers import ModelSerializer, ImageField
from proauto.models import Brend, Country, Auto


class BrendListSerializer(ModelSerializer):
    class Meta:
        model = Brend
        fields = ('title',  'slug', 'content', 'previewImg')


class CountrySerializer(ModelSerializer):
    previewImg = ImageField(source='flagImg', read_only=True)
    class Meta:
        model = Country
        fields = ('title', 'slug', 'content', 'cat', 'previewImg')


class AutoSerializer(ModelSerializer):
    class Meta:
        model = Auto
        fields = ('title', 'slug', 'content', 'cat', 'previewImg')




