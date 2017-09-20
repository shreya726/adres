from . import views

from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
                  url(r'^$', views.home, name='home'),
                  url(r'^score/$', views.score, name='score'),
                  url(r'^script/$', views.script, name='script'),
                  url(r'^about/', views.about),
                  url(r'^adres/', views.index),
                  url(r'^upload/', views.upload),
                  url(r'^admin/', admin.site.urls),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
