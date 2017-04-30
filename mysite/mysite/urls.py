from django.conf.urls import include, url
from django.contrib import admin

from django.conf.urls import patterns, include, url
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
	url(r'^$', views.index),
    url(r'^about/', views.about),
    url(r'^adres/', include('adres.urls')),
    url(r'^upload/', views.upload),
    url(r'^admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)