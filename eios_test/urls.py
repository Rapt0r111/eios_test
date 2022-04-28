
from django.views.static import serve

from eios_test import settings
from django.urls import path,include
from django.contrib import admin
from django.conf.urls.static import static

urlpatterns = [
    path('admin/',admin.site.urls),
    path('', include('main.urls')),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
handler404 = "main.views.page_not_found_view"

if settings.DEBUG:
    urlpatterns += [path('__debug__/', include('debug_toolbar.urls'))]


