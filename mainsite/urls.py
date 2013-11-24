from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from . import views

urlpatterns = patterns(
    '',
    url(r'^$', views.index, name="index"),
    url(r'^product/$', views.product, name="index"),
    url(r'^generater/$', views.generater, name="index"),
    url(r'^create/$', views.create, name="create"),
    url(r'^page/$', views.page, name="create"),
    )
