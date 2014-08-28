from django.contrib.gis.db import models


class DayOfWeek(models.Model):
    day_number = models.IntegerField()
    short_name = models.CharField(max_length=3)
    name = models.CharField(max_length=9)


class SignType(models.Model):
    code = models.CharField(max_length=2)
    label = models.CharField(max_length=20)


class SignArchetype(models.Model):
    start_time = models.TimeField()
    end_time = models.TimeField()

    start_day = models.IntegerField()
    end_day = models.IntegerField()

    # AKA "God Mode"
    allow_permit_override = models.BooleanField()

    requires_pay_ticket = models.BooleanField()
    requires_pay_meter = models.BooleanField()
    requires_disability_permit = models.BooleanField()

    duration_mins = models.IntegerField()

    type = models.ForeignKey(SignType)

    def requires_pay(self):
        return self.requires_pay_meter or self.requires_pay_ticket


class ParkingBay(models.Model):
    street_marker = models.CharField(max_length=10)
    geom = models.PointField()

    sign_archetypes = models.ManyToManyField(SignArchetype, through='ParkingBaySignArchetypeRelationship')

    objects = models.GeoManager()

    def __str__(self):
        return self.street_marker


class ParkingBaySignArchetypeRelationship(models.Model):
    parking_bay = models.ForeignKey(ParkingBay)
    sign_archetype = models.ForeignKey(SignArchetype)
    last_seen = models.DateTimeField()


class ParkingEvent(models.Model):
    parking_bay = models.ForeignKey(ParkingBay)
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()

    def __str__(self):
        return "Parking event: %s (from %s to %s)" % (self.parking_bay, self.arrival_time, self.departure_time)
