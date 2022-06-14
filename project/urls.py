from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin-panel/', admin.site.urls),
    path("", include("home.urls")),
    path("accounts/", include("accounts.urls")),
]
handler404 = 'home.views.notfound404'

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) 
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)