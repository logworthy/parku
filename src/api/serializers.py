from rest_framework_gis.serializers import GeoFeatureModelSerializer
from api.models import ParkingBay, AggregateGridCell, AggregateParkingBays


class ParkingBaySerializer(GeoFeatureModelSerializer):
    class Meta:
        model = ParkingBay
        geo_field = 'geom'
        fields = ('street_marker',)


#class SignArchetypeSerializer():


class AggregateParkingBaysSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = AggregateParkingBays
        geo_field = 'center'
        fields = ('zoom_level', 'bay_count')

class AggregateGridCellSerializer(GeoFeatureModelSerializer):
    class Meta:
        model = AggregateGridCell
        geo_field = 'geom'
        fields = ('zoom_level',)
