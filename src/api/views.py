from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.renderers import JSONRenderer
from api.models import ParkingBay, AggregateParkingBays, SignArchetype, ParkingBaySignArchetypeRelationship
from api.serializers import AggregateParkingBaysSerializer, ParkingBaySerializer, SignArchetypeSerializer, ParkingBaySignArchetypeRelationshipSerializer


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


@api_view(['GET'])
def bay_list(request):
    if request.method == 'GET':
        bays = ParkingBay.objects.all()[:100]
        serializer = ParkingBaySerializer(bays, many=True)
        return Response(serializer.data)


@api_view(['GET'])
def sign_archetype_list(request):
    if request.method == 'GET':
        signs = SignArchetype.objects.all()
        serializer = SignArchetypeSerializer(signs, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def parkingbaysignarchetyperelationship_detail(request, pk):
    try:
        pbsar = ParkingBaySignArchetypeRelationship.objects.get(id=pk)
    except ParkingBaySignArchetypeRelationship.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ParkingBaySignArchetypeRelationshipSerializer(pbsar)
        return Response(serializer.data)

@api_view(['GET'])
def bay_detail(request, pk):
    try:
        bay = ParkingBay.objects.get(id=pk)
    except ParkingBay.DoesNotExist:
        return HttpResponse(status=404)

    if request.method == 'GET':
        serializer = ParkingBaySerializer(bay)
        return Response(serializer.data)
