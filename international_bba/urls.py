from django.urls import path, include
from django.conf.urls import url
from django.conf.urls.static import static
from . import settings
from django.contrib import admin
from django.views.static import serve


urlpatterns = [
    path('admin/', admin.site.urls),
    path('static/<path>', serve, {'document_root', settings.STATIC_ROOT}),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('', include('ibba_app.urls'), name="ibba_app"),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
