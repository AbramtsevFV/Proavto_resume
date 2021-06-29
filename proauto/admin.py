from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import *


class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug', 'parent_id')
    prepopulated_fields = {'slug': ('name',)}

class AutoAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'short_content', 'production_date', 'get_html_previewImg', 'get_html_main', 'cat')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}

    def get_html_previewImg(self, object):
        if object.previewImg:
            return mark_safe(f"<img src = {object.previewImg.url} width=50>")
    get_html_previewImg.short_description = 'Привью'

    def get_html_main(self, object):
        if object.mainImg:
            return mark_safe(f"<img src = {object.mainImg.url} width=50>")
    get_html_main.short_description = 'Основная картинка'

class BrendAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'content', 'previewImg', 'cat')
    prepopulated_fields = {'slug': ('title',)}

class CountrAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug', 'content', 'get_html_flagImg', 'cat')
    prepopulated_fields = {'slug': ('title',)}

    def get_html_flagImg(self, object):
        if object.flagImg:
            return mark_safe(f"<img src = {object.flagImg.url}>")
    get_html_flagImg.short_description=" Флаг страны"


class FeedbackAdmin(admin.ModelAdmin):
    list_display =('name', 'title', 'massage', 'time_create')


admin.site.register(Menu, MenuAdmin)
admin.site.register(Auto, AutoAdmin)
admin.site.register(Brend, BrendAdmin)
admin.site.register(Country, CountrAdmin)
admin.site.register(Feedback,FeedbackAdmin)

admin.site.site_title = 'Адмиистрирование  сайта про авто'
admin.site.site_header = 'Панель управления сайта про авто'