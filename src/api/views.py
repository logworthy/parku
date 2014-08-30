from rest_framework import status, generics, viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from django.http import HttpResponse, Http404
from api.models import ParkingBay, AggregateParkingBays, SignArchetype, ParkingBaySignArchetypeRelationship, DayOfWeek, SignType
from api.serializers import AggregateParkingBaysSerializer, ParkingBaySerializer, SignArchetypeSerializer, DayOfWeekSerializer, SignTypeSerializer 
#ParkingBaySignArchetypeRelationshipSerializer

@api_view(('GET',))
def api_root(request, format=None):
    """
    parku API created for infraHack 2014.

    For more details on the project please [see here][ref].

    [ref]: https://github.com/logworthy/parku
    """
    return Response({
        'bays': reverse('bay-list', request=request, format=format),
        'sign_archetypes': reverse('sign_archetype-list', request=request, format=format),
        'reference': {
            'days_of_week': reverse('day_of_week-list', request=request, format=format),
            'sign_types': reverse('sign_type-list', request=request, format=format),
        }
    })

MAX_ZOOM = 17
MIN_ZOOM = 13

class AggregateBayListView(APIView):
    """
    An aggregation of parking bays.  A point representing the number of bays within a rectangluar region around that point.
    """
    def get(self, request, zoom_level):
        zoom = max(min(int(zoom_level), MAX_ZOOM), MIN_ZOOM)        
        sql = "SELECT ( random() * 100000 )::int as id, cell.zoom_level, ST_Centroid( cell.geom ) as center, count( bay.id ) as bay_count FROM api_aggregategridcell AS cell, api_parkingbay AS bay WHERE ST_Within( bay.geom, cell.geom ) AND cell.zoom_level = %d GROUP BY cell.id" % zoom
        cells = AggregateParkingBays.objects.raw(sql)
        serializer = AggregateParkingBaysSerializer(cells, many=True)
        return Response(serializer.data)

class ParkingBayViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A Parking Bay is represented as a geographic point, uniquely identifiable by a street marker.
    """
    queryset = ParkingBay.objects.all()
    serializer_class = ParkingBaySerializer
    paginate_by = 10

class SignArchetypeViewSet(viewsets.ReadOnlyModelViewSet):    
    """
    A Sign Archetype is a set of parking regulations (e.g. 2P Ticket) that apply for a specified period of time (e.g. M-F).

    A Parking Bay may be regulated by one or more Sign Archetypes (e.g. one set for M-F, another for S-S).

    Sign Archetypes are reused throughout the city, so multiple Parking Bays may link to the same Sign Archetype.
    """
    queryset = SignArchetype.objects.all()
    serializer_class = SignArchetypeSerializer
    paginate_by = 10

class SignTypeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A Sign Type refers to a general category of sign, (e.g. P, Loading Zone, Clearway)
    """
    queryset = SignType.objects.all()
    serializer_class = SignTypeSerializer

class DayOfWeekViewSet(viewsets.ReadOnlyModelViewSet):
    """
    A Day of Week enumeration.  0 = Monday, 1 = Tuesday, etc.
    """
    queryset = DayOfWeek.objects.all()
    serializer_class = DayOfWeekSerializer