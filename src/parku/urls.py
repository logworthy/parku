from django.conf.urls import patterns, include, url
from django.contrib import admin
from api.views import bay_list, bay_detail, sign_archetype_list, parkingbaysignarchetyperelationship_detail
from web import views


admin.autodiscover()


urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/bays$', bay_list),
    url(r'^api/sign_archetypes$', sign_archetype_list),
    url(r'^api/bays/(?P<pk>[0-9]+)/$', bay_detail, name='bay-detail'),
    url(r'^api/parkingbaysignarchetyperelationships/(?P<pk>[0-9]+)/$', 
    	parkingbaysignarchetyperelationship_detail,
    	name='parkingbaysignarchetyperelationship-detail'),
    url(r'^$', views.index, name='home'),
)

