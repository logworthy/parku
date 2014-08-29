from rest_framework_gis.serializers import GeoFeatureModelSerializer
from api.models import ParkingBay


class ParkingBaySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ParkingBay
        geo_field = 'geom'
        fields = ('street_marker',)

#class SignArchetypeSerializer():
