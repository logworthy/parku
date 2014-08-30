from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from api.models import (ParkingBay, SignArchetype, ParkingBaySignArchetypeRelationship, AggregateGridCell, AggregateParkingBays, DayOfWeek, SignType)

class DayOfWeekSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='day_of_week-detail', format='html')
    class Meta:
        model = DayOfWeek
        fields = ('url', 'day_number', 'short_name', 'name')

class SignTypeSerializer(serializers.ModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='sign_type-detail', format='html')
    class Meta:
        model = SignType
        fields = ('url', 'code', 'label')

class SignArchetypeSerializer(serializers.ModelSerializer):
        url = serializers.HyperlinkedIdentityField(view_name='sign_archetype-detail', format='html')
        start_day = serializers.HyperlinkedRelatedField(view_name='day_of_week-detail')
        end_day = serializers.HyperlinkedRelatedField(view_name='day_of_week-detail')
        type = serializers.HyperlinkedRelatedField(view_name='sign_type-detail')


        class Meta:
            model = SignArchetype
            fields = ('url',
            'id',
            'start_time',
            'end_time',
            'start_day',
            'end_day',
            'any_other_time',
            'allow_permit_override',
            'requires_pay_ticket',
            'requires_pay_meter',
            'requires_disability_permit',
            'duration_mins',
            'type',
            'raw_sign_text')

class ParkingBaySerializer(GeoFeatureModelSerializer):
    url = serializers.HyperlinkedIdentityField(view_name='bay-detail', format='html')
    sign_archetypes = serializers.HyperlinkedRelatedField(many=True, view_name='sign_archetype-detail')

    class Meta:
        model = ParkingBay
        geo_field = 'geom'
        fields = ('url', 'street_marker','id','sign_archetypes')


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
