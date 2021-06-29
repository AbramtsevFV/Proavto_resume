from django.db import models
from django.template.defaultfilters import truncatechars
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey
from ckeditor_uploader.fields import RichTextUploadingField

class Brend(models.Model):
    title = models.CharField(max_length=255, verbose_name='Бренд')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = RichTextUploadingField(verbose_name='Содержание страницы')
    previewImg = models.ImageField(upload_to='photo_auto/brend', verbose_name='Логотип')
    cat = models.ForeignKey('Menu', on_delete=models.PROTECT, verbose_name='Принадлежность к стране')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('brend', kwargs={'brend_slug': self.slug})

    class Meta:
            verbose_name = "Производители автомобилей"
            verbose_name_plural = "Производители автомобилей"

class Auto(models.Model):

    title = models.CharField(max_length=255, verbose_name='Бренд')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = RichTextUploadingField(verbose_name='Содержание страницы')
    production_date = models.IntegerField(verbose_name='Год начала производства')
    previewImg = models.ImageField(upload_to='photo_auto/preview', verbose_name='Картинка предпросмотра')
    mainImg = models.ImageField(upload_to='photo_auto/mainimg', verbose_name='Основная картинка')
    cat = models.ForeignKey('Brend', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('auto', kwargs={'auto_slug': self.slug})

    class Meta:
            verbose_name = "Модели автомобилей"
            verbose_name_plural = "Модели автомобилей"
            ordering = ['production_date', 'title']

    @property
    def short_content(self):
        return truncatechars(self.content, 100)


class Country(models.Model):
    title = models.CharField(max_length=255, verbose_name='Страна')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    content = RichTextUploadingField(verbose_name='Содержание страницы')
    flagImg = models.ImageField(upload_to='photo_auto/flag', verbose_name='Флаг страны')
    cat = models.ForeignKey('Menu', on_delete=models.PROTECT, verbose_name='Категория')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('country', kwargs={'country_slug': self.slug})

    class Meta:
        verbose_name = "Страна"
        verbose_name_plural = "Страны"


class Menu(MPTTModel):
    name = models.CharField(max_length=50, unique=True, verbose_name='Пункт меню')
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name='URL')
    parent = TreeForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='Родители')

    class MPTTMeta:
        order_insertion_by = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        """
        Настройки для корректного отображения уровней меню
        """
        if self.get_level() == 0:
            return reverse('country', kwargs={'country_slug': self.slug})
        else:
            return reverse('brend', kwargs={'brend_slug': self.slug})

    class Meta:
        verbose_name = "Главное мню"
        verbose_name_plural = "Главное мню"



class Feedback(models.Model):
    name = models.CharField(max_length=200, verbose_name='Ваше имя')
    email = models.EmailField(max_length=200, verbose_name='Email')
    title = models.CharField(max_length=50, verbose_name='Тема обрщения')
    massage = models.TextField(max_length=1500, verbose_name='Текст обращения')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')

    def __str__(self):
        return self.email
