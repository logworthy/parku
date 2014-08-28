from django.conf.urls import patterns, include, url
from web import views

from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^$', views.index, name='home'),
                       url(r'^admin/', include(admin.site.urls)),
)
