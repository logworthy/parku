from django.conf.urls import patterns, include, url
from django.contrib import admin
from api.views import bay_list, bay_detail, aggregate_bay_list
from web import views


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/bays$', bay_list),
    url(r'^api/bays/aggregate/(?P<zoom_level>[0-9]+)$', aggregate_bay_list),
    url(r'^api/bays/(?P<pk>[0-9]+)/$', bay_detail),
    url(r'^$', views.index, name='home'),
)

