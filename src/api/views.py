from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from api.models import ParkingBay
from api.serializers import ParkingBaySerializer


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