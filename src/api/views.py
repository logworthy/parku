from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from api.models import ParkingBay, SignArchetype, ParkingBaySignArchetypeRelationship
from api.serializers import (ParkingBaySerializer, SignArchetypeSerializer,
 ParkingBaySignArchetypeRelationshipSerializer)


class JSONResponse(HttpResponse):
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


#@csrf_exempt
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