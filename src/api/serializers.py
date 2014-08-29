from rest_framework_gis.serializers import GeoFeatureModelSerializer
from rest_framework import serializers
from api.models import (ParkingBay, SignArchetype, 
ParkingBaySignArchetypeRelationship)

class SignArchetypeSerializer(serializers.ModelSerializer):
        class Meta:
            model = SignArchetype
            fields = ('id',
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

class ParkingBaySignArchetypeRelationshipSerializer(serializers.ModelSerializer):
        class Meta:
            model = ParkingBaySignArchetypeRelationship
            fields = ('parking_bay',
            'sign_archetype',
            'last_seen')

class ParkingBaySerializer(GeoFeatureModelSerializer):
    #parkingbaysignarchetyperelationship_set = ParkingBaySignArchetypeRelationshipSerializer(many=True)
    parkingbaysignarchetyperelationship_set = serializers.HyperlinkedRelatedField(many=True, read_only=True
        , view_name='parkingbaysignarchetyperelationship-detail')

    class Meta:
        model = ParkingBay
        geo_field = 'geom'
        fields = ('street_marker','id','parkingbaysignarchetyperelationship_set')
