from django.conf.urls import patterns, include, url
from django.contrib import admin
from api.views import bay_list
from web import views


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/bays$', bay_list),
    url(r'^$', views.index, name='home'),
)

