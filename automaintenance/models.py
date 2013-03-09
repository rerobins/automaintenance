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
    slug = models.SlugField()
    car_type = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, related_name='+')

    def __str__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
            return('auto_maintenance_car_detail', [str(self.slug)])


class Trip(models.Model):
    slug = models.SlugField()
    car = models.ForeignKey(Car, related_name='+')
    name = models.CharField(max_length=100)
    description = models.TextField()
    start = models.DateTimeField()
    end = models.DateTimeField(null=True)

    def __unicode__(self):
        return self.name

    @permalink
    def get_absolute_url(self):
        return('auto_maintenance_trip_view', [str(self.car.slug), str(self.slug)])


class Maintenance(models.Model):
    slug = models.SlugField()
    date = models.DateTimeField(unique=True)
    car = models.ForeignKey(Car)
    trip = models.ForeignKey(Trip, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    mileage = models.PositiveIntegerField()
    description = models.TextField(blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, blank=True)

    def __unicode__(self):
        return "Maintenance: %s" % self.date

    def __cmp__(self, other):
        if self.date < other.date:
            return -1
        elif self.date > other.date:
            return 1
        return 0

    @permalink
    def get_absolute_url(self):
        return('auto_maintenance_view_record', [str(self.car.slug),str(self.slug)])


class GasolinePurchase(Maintenance):
    tank_mileage = models.DecimalField(max_digits=6, decimal_places=3)
    price_per_gallon = models.DecimalField(max_digits=6, decimal_places=3)
    gallons = models.DecimalField(max_digits=7, decimal_places=3)

    @permalink
    def get_absolute_url(self):
        return('auto_gasolinepurchase_view_record', [str(self.car.slug),str(self.slug)])

    def __unicode__(self):
        return "Gasoline Purchase: %s" % self.date


class OilChange(Maintenance):

    @permalink
    def get_absolute_url(self):
        return('auto_oilchange_view_record', [str(self.car.slug),str(self.slug)])

    def __unicode__(self):
        return "Oil Change: %s" % self.date


class ScheduledMaintenance(Maintenance):
    def __unicode__(self):
        return "Scheduled Maintenance: %s" % self.date

