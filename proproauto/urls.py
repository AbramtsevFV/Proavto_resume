"Мы здесь в качестве параметра указываем строку, в которой сначала "
# записываем имя приложения и через точку файл urls, где будут прописаны
# маршруты приложения women.
# Ну а дальше все просто. Мы добавляем в
# приложение новый файл urls.py и в нем формируем список urlpatterns:"
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from proauto.views import *
from proproauto import settings


urlpatterns = [
    path('admin/', admin.site.urls),
    path('captcha/', include('captcha.urls')),
    path('', include('proauto.urls')),
    url(r'^ckeditor/', include('ckeditor_uploader.urls')),
    path('api/v1/', include('api_for_proauto.urls')),
    path('telegram/', include('tg_bot.urls'))

]

# При включонном режиме отладки к urlpatterns добовляется
# маршрут для статических  данных граффических файлов
# это только в отладочном режиме на реальных серверах процесс настроен
# Для запускаDEBUG настроек прописывается
if settings.DEBUG:
    import debug_toolbar
    # две строки прописываются если не работает
    import mimetypes
    mimetypes.add_type("application/javascript", ".js", True)

    import mimetypes
    mimetypes.add_type("application/javascript", ".js", True)

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
# так же есть handler500, handler403, handler400
