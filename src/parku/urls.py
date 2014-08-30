from django.conf.urls import patterns, include, url
from django.contrib import admin
from api.views import api_root
from api import views as api_views
from web import views
from rest_framework.routers import SimpleRouter

ref_router = SimpleRouter()
ref_router.register(r'days_of_week', api_views.DayOfWeekViewSet, 'day_of_week')
ref_router.register(r'sign_types', api_views.SignTypeViewSet, 'sign_type')

api_router = SimpleRouter()
api_router.register(r'bays', api_views.ParkingBayViewSet, 'bay')
api_router.register(r'sign_archetypes', api_views.SignArchetypeViewSet, 'sign_archetype')

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    url(r'^api/$', api_root),
    url(r'^api/', include(api_router.urls)),
    url(r'^api/reference/', include(ref_router.urls)),
    url(r'^api/bays/aggregate/(?P<zoom_level>[0-9]+)$', api_views.AggregateBayListView.as_view()),
    url(r'^$', views.index, name='home'),
)

