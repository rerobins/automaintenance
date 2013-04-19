##
# Automaintenance.  Django app to track automaintenance records.
# Copyright (C) 2012 Robert Robinson
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
##
from django.db import models

from django.db.models import permalink
from django.contrib.auth.models import User


class Car(models.Model):
    """
        Car model that is the parent object for all of the maintenance records.
    """
    slug = models.SlugField()
    car_type = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, related_name='+')

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        """
            Return the name of the object as the default print out.
        """
        return self.name

    @permalink
    def get_absolute_url(self):
        """
            Override the absolute url for this object.
        """
        return('auto_maintenance_car_detail', [str(self.slug)])


class Trip(models.Model):
    """
        Trips are a means of organizing maintenance records.  This allows for a
        user to organize the records by a trip that the records took place
        during.
    """
    slug = models.SlugField()
    car = models.ForeignKey(Car, related_name='+')
    name = models.CharField(max_length=100)
    description = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)

    class Meta:
        """
            Meta class that overrides the models basic attributes.
        """
        ordering = ['name']

    def __unicode__(self):
        """
            Return the name of the object as the default print out.
        """
        return self.name

    @permalink
    def get_absolute_url(self):
        """
            Override the url for the trip detail view.
        """
        return('auto_maintenance_trip_view', [str(self.car.slug),
            str(self.slug)])


class MaintenanceBase(models.Model):
    """
        Maintenance root object that contains date, car, location, mileage, and
        cost fields for any of the maintenance record values.
    """
    date = models.DateTimeField(unique=True)
    car = models.ForeignKey(Car)
    trip = models.ForeignKey(Trip, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    mileage = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2,
        blank=True)

    class Meta:
        """
            Mark the model as being an abstract model for the rest of the
            maintenance type objects.
        """
        abstract = True
        ordering = ['date']
        get_latest_by = 'date'

    def __unicode__(self):
        """
            Means of printing out basic information for this record.
        """
        return "Maintenance: %s" % self.date

    def __cmp__(self, other):
        """
            Basic comparison operator for all records that will sort based on
            the date values.
        """
        if self.date < other.date:
            return -1
        elif self.date > other.date:
            return 1
        return 0

    @permalink
    def get_absolute_url(self):
        """
            Override the url object for this record.
        """
        return('auto_maintenance_view_record', [str(self.car.slug),
            str(self.pk)])


class GasolinePurchase(MaintenanceBase):
    """
        Gasoline purchase instance of a maintenance record.  Includes values
        for amount of gasoline, and price per unit.
    """
    tank_mileage = models.DecimalField(max_digits=6, decimal_places=3)
    price_per_unit = models.DecimalField(max_digits=6, decimal_places=3)
    fuel_amount = models.DecimalField(max_digits=7, decimal_places=3)
    filled_tank = models.BooleanField(default=True)

    @permalink
    def get_absolute_url(self):
        """
            Absolute URL for the detailed record.
        """
        return('auto_gasolinepurchase_view_record', [str(self.car.slug),
            str(self.pk)])

    def __unicode__(self):
        """
            Overrides the maintenance unicode string to show that this record
            was a gasoline record.
        """
        return "Gasoline Purchase: %s" % self.date


class OilChange(MaintenanceBase):
    """
        Oil Change instance of a maintenance record.  Just used to tag this
        record as the oil change.
    """

    @permalink
    def get_absolute_url(self):
        """
            Absolute URL for the detailed record.
        """
        return('auto_oilchange_view_record', [str(self.car.slug),
            str(self.pk)])

    def __unicode__(self):
        """
            Overrides the maintenance unicode string to show that the record
            was an oil change record.
        """
        return "Oil Change: %s" % self.date


class Maintenance(MaintenanceBase):
    """
        Other Maintenance record.
    """

    def __unicode__(self):
        """
            Overrides the mainentance unicode string to show that the record
            was for mainteance.
        """
        return "Maintenance: %s" % self.date
