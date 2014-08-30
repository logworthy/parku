from rest_framework import status, generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.reverse import reverse
from django.http import HttpResponse, Http404
from rest_framework.renderers import JSONRenderer
from api.models import ParkingBay, AggregateParkingBays, SignArchetype, ParkingBaySignArchetypeRelationship, DayOfWeek, SignType
from api.serializers import AggregateParkingBaysSerializer, ParkingBaySerializer, SignArchetypeSerializer, DayOfWeekSerializer, SignTypeSerializer 
#ParkingBaySignArchetypeRelationshipSerializer

@api_view(('GET',))
def api_root(request, format=None):
    return Response({
        'bays': reverse('bay-list', request=request, format=format),
        'sign_archetypes': reverse('sign_archetype-list', request=request, format=format),
        'reference': {
            'days_of_week': reverse('day_of_week-list', request=request, format=format),
            'sign_types': reverse('sign_type-list', request=request, format=format),
        }
    })

class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@api_view(['GET'])
def aggregate_bay_list(request, zoom_level):
    if request.method == 'GET':

        zoom = int(zoom_level)

        if zoom > 17:
            zoom = 17
        elif zoom < 13:
            zoom = 13

        sql = "SELECT ( random() * 100000 )::int as id, cell.zoom_level, ST_Centroid( cell.geom ) as center, count( bay.id ) as bay_count FROM api_aggregategridcell AS cell, api_parkingbay AS bay WHERE ST_Within( bay.geom, cell.geom ) AND cell.zoom_level = %d GROUP BY cell.id" % zoom
        cells = AggregateParkingBays.objects.raw(sql)

        serializer = AggregateParkingBaysSerializer(cells, many=True)
        return Response(serializer.data)


class BayList(generics.ListAPIView):
    queryset = ParkingBay.objects.all()
    serializer_class = ParkingBaySerializer
    paginate_by = 10

class BayDetail(generics.RetrieveAPIView):
    queryset = ParkingBay.objects.all()
    serializer_class = ParkingBaySerializer

class SignArchetypeList(generics.ListAPIView):
    queryset = SignArchetype.objects.all()
    serializer_class = SignArchetypeSerializer
    paginate_by = 10

class SignArchetypeDetail(generics.RetrieveAPIView):
    queryset = SignArchetype.objects.all()
    serializer_class = SignArchetypeSerializer
    paginate_by = 10

class SignTypeList(generics.ListAPIView):
    queryset = SignType.objects.all()
    serializer_class = SignTypeSerializer
    paginate_by = 10

class SignTypeDetail(generics.RetrieveAPIView):
    queryset = SignType.objects.all()
    serializer_class = SignTypeSerializer
    paginate_by = 10

class DayOfWeekList(generics.ListAPIView):
    queryset = DayOfWeek.objects.all()
    serializer_class = DayOfWeekSerializer
    paginate_by = 10

class DayOfWeekDetail(generics.RetrieveAPIView):
    queryset = DayOfWeek.objects.all()
    serializer_class = DayOfWeekSerializer
    paginate_by = 10

@api_view(['GET'])
def parkingbaysignarchetyperelationship_detail(request, pk):
    try:
        pbsar = ParkingBaySignArchetypeRelationship.objects.get(id=pk)
    except ParkingBaySignArchetypeRelationship.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ParkingBaySignArchetypeRelationshipSerializer(pbsar)
        return Response(serializer.data)
