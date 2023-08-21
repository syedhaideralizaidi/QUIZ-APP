from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("base.urls")),
    path("__debug__/", include("debug_toolbar.urls")) , # ToDo: this application is not available in the installed application
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
