from django.conf.urls import patterns, include, url
from django.contrib import admin
from api.views import parkingbaysignarchetyperelationship_detail, aggregate_bay_list, api_root
from api import views as api_views
from web import views


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/$', api_root),

    url(r'^api/bays$', api_views.BayList.as_view(), name='bay-list'),
    url(r'^api/bays/(?P<pk>[0-9]+)/$', api_views.BayDetail.as_view(), name='bay-detail'),
    url(r'^api/bays/aggregate/(?P<zoom_level>[0-9]+)$', aggregate_bay_list),

    url(r'^api/sign_archetypes$', api_views.SignArchetypeList.as_view(), name='sign_archetype-list'),
    url(r'^api/sign_archetypes/(?P<pk>[0-9]+)/$', api_views.SignArchetypeDetail.as_view(), name='sign_archetype-detail'),

    url(r'^api/parkingbaysignarchetyperelationships/(?P<pk>[0-9]+)/$',
    	parkingbaysignarchetyperelationship_detail,
    	name='parkingbaysignarchetyperelationship-detail'),
    url(r'^$', views.index, name='home'),
)

