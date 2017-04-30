from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^upload/$', views.score, name='score'),
    url(r'^script/$', views.script, name='script')
]