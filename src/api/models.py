from django.contrib.gis.db import models


class ParkingBay(models.Model):
    street_marker = models.CharField(max_length=10)
    geom = models.PointField()

    objects = models.GeoManager()

    def __str__(self):
        return self.street_marker


class ParkingEvent(models.Model):
    parking_bay = models.ForeignKey(ParkingBay)
    arrival_time = models.DateTimeField()
    departure_time = models.DateTimeField()

    def __str__(self):
        return "Parking event: %s (from %s to %s)" % (self.parking_bay, self.arrival_time, self.departure_time)