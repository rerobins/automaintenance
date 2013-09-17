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
from django.template.defaultfilters import date
from django.conf import settings
from django.core.urlresolvers import reverse
from django.utils.safestring import mark_safe

import pytz

from datetime import datetime


# Time zone choices for all of the record date time values.
timezone_choices = [(time_zone, time_zone)
    for time_zone in pytz.common_timezones]

MILEAGE_UNITS_MILES = 'mi'
MILEAGE_UNITS_KILOMETERS = 'km'    
    
MILEAGE_UNITS = (
                 (MILEAGE_UNITS_MILES, 'Miles'),
                 (MILEAGE_UNITS_KILOMETERS, 'Kilometers')
                )

FUEL_UNITS_US_GALLONS = 'us_gal'
FUEL_UNITS_IMP_GALLONS = 'imp_gal'
FUEL_UNITS_LITERS = 'l'

FUEL_UNITS = (
                (FUEL_UNITS_US_GALLONS, 'Gallons (US)'),
                (FUEL_UNITS_IMP_GALLONS, 'Gallons (IMP)'),
                (FUEL_UNITS_LITERS, 'Liters')
             )

DEFAULT_CURRENCY = 'us_dollars'

CURRENCY_UNITS = (
                (DEFAULT_CURRENCY, '$'),
                ('uk_pounds', mark_safe('&pound;')),
                ('euros', mark_safe('&euro;')),
                ('generic_currency', mark_safe('&curren;')),
             )

PAYMENT_TYPES = (
    ('taxes', 'Taxes'),
    ('association', 'Automobile Association'),
    ('parking', 'Parking'),
    ('fines', 'Fines'),
    ('insurance', 'Insurance'),
    ('loan', 'Loan Interest'),
    ('carwash', 'Car Wash'),
    ('other', 'Other')
)

DEFAULT_PAYMENT_TYPE = 'other'


def date_sorting(first, second):
    """
            Basic comparison function for all records that will sort based on
            the date values.
        """
    return_value = 0

    if first.date < second.date:
        return_value = -1
    elif first.date > second.date:
        return_value = 1

    return return_value


class Car(models.Model):
    """
        Car model that is the parent object for all of the maintenance records.
    """
    slug = models.SlugField()
    car_type = models.CharField(max_length=50, default="Unknown Type")
    name = models.CharField(max_length=50)
    owner = models.ForeignKey(User, related_name='+')
    mileage_unit = models.CharField(max_length=2, choices=MILEAGE_UNITS, 
                                    default=MILEAGE_UNITS_MILES)
    fuel_unit = models.CharField(max_length=10, choices=FUEL_UNITS,
                                 default=FUEL_UNITS_US_GALLONS)
    city_rate = models.DecimalField(max_digits=5, decimal_places=2,
                                    default=24.0)
    highway_rate = models.DecimalField(max_digits=5, decimal_places=2,
                                       default=27.0)
    currency = models.CharField(max_length=20, choices=CURRENCY_UNITS,
                                default=DEFAULT_CURRENCY)

    class Meta:
        ordering = ['name']

    def __unicode__(self):
        """
            Return the name of the object as the default print out.
        """
        return self.name
    
    def get_distance_table_header(self):
        """
            Return a string that can be used for a mileage header.
        """
        if self.mileage_unit == MILEAGE_UNITS_MILES:
            return "Total Miles"
        elif self.mileage_unit == MILEAGE_UNITS_KILOMETERS:
            return "Total Km"
        
    def get_distance_per_fuel(self):
        """
            Return a distance per fuel label.
        """
        if self.mileage_unit == MILEAGE_UNITS_MILES:
            if self.fuel_unit == FUEL_UNITS_US_GALLONS:
                return "MPG"
            elif self.fuel_unit == FUEL_UNITS_IMP_GALLONS:
                return "MPG(Imp)"
            elif self.fuel_unit == FUEL_UNITS_LITERS:
                return "MPL"
        elif self.mileage_unit == MILEAGE_UNITS_KILOMETERS:
            if self.fuel_unit == FUEL_UNITS_LITERS:
                return "KPL"
            elif self.fuel_unit == FUEL_UNITS_US_GALLONS:
                return "KPG"
            elif self.fuel_unit == FUEL_UNITS_IMP_GALLONS:
                return "KPG(Imp)"


    @permalink
    def get_absolute_url(self):
        """
            Override the absolute url for this object.
        """
        return('auto_maintenance_car_detail', [str(self.slug)])   
    
    def get_maintenance_list(self, start_date=None, end_date=None, trip=None):
        """
            Returns a list of maintenance records for the car model provided.
        """ 
        # Populate the maintenance list for this car
        gasoline = self.maintenance_query(GasolinePurchase, start_date=start_date, end_date=end_date, trip=trip)
        
        oilchange = self.maintenance_query(OilChange, start_date, end_date, trip)
                
        maintenance = self.maintenance_query(Maintenance, start_date, end_date, trip)

        payment = self.maintenance_query(Payment, start_date, end_date, trip)
        
        maintenance_list = list(gasoline) + list(oilchange) + list(maintenance) + list(payment)
        maintenance_list = sorted(maintenance_list, cmp=date_sorting)

        return maintenance_list
    
    def maintenance_query(self, object_type, start_date=None, end_date=None, trip=None):
        """
            Queries the maintenance records based on fields provided.
        """
        maintenance = object_type.objects.filter(car=self)
        if start_date is not None:
            maintenance = maintenance.filter(date__gte=start_date)
        if end_date is not None:
            maintenance = maintenance.filter(date__lte=end_date)
        if trip is not None:
            maintenance = maintenance.filter(trip=trip)
            
        return maintenance
        

class Trip(models.Model):
    """
        Trips are a means of organizing maintenance records.  This allows for a
        user to organize the records by a trip that the records took place
        during.
    """
    slug = models.SlugField()
    car = models.ForeignKey(Car, related_name='+')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
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
        return "%s - %s" % (date(self.start, "Y-m-d"), self.name)

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
    date = models.DateTimeField(unique=True, default=datetime.now)
    date_timezone = models.CharField(max_length=50, choices=timezone_choices, 
                                     default=settings.TIME_ZONE)
    car = models.ForeignKey(Car)
    trip = models.ForeignKey(Trip, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    mileage = models.PositiveIntegerField(default=0)
    description = models.TextField(blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2,
        blank=True, default=0.0)

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
    
    def human_readable_type(self):
        """ 
            Returns a human readable type information for this object type.
        """
        return "Abstract"

    def get_absolute_url(self):
        """
            Override the url object for this record.
        """
        return reverse('auto_maintenance_view_record',
            kwargs={'car_slug': self.car.slug,
                    'pk': self.pk})        
        
    def get_edit_url(self):
        """
            Define a url object for editing maintenance records.
        """
        return reverse('auto_maintenance_edit_scheduled_maintenance',
            kwargs={'car_slug': self.car.slug,
                    'pk': self.pk})
    
    def get_delete_url(self):
        """
            Define a url object for deleting maintenance records. 
        """
        return reverse('auto_maintenance_delete_scheduled_maintenance',
            kwargs={'car_slug': self.car.slug,
                    'pk': self.pk})
            

class GasolinePurchase(MaintenanceBase):
    """
        Gasoline purchase instance of a maintenance record.  Includes values
        for amount of gasoline, and price per unit.
    """
    tank_mileage = models.DecimalField(max_digits=6, decimal_places=3, default=0.0)
    price_per_unit = models.DecimalField(max_digits=6, decimal_places=3, default=0.0)
    fuel_amount = models.DecimalField(max_digits=7, decimal_places=3, default=0.0)
    filled_tank = models.BooleanField(default=True)

    def __unicode__(self):
        """
            Overrides the maintenance unicode string to show that this record
            was a gasoline record.
        """
        return "Gasoline Purchase: %s" % self.date
    
    def efficency(self):
#         if self.filled_tank:
#             return 0.0
        return self.tank_mileage / self.fuel_amount
    
    def human_readable_type(self):
        """ 
            Returns a human readable type information for this object type.
        """
        return "Gasoline"
    
    def get_absolute_url(self):
        """
            Absolute URL for the detailed record.
        """
        return reverse('auto_gasolinepurchase_view_record',
                       kwargs={'car_slug': self.car.slug,
                               'pk': self.pk})
    
    def get_edit_url(self):
        """
            Define a url object for editing gasoline records.
        """
        return reverse('auto_maintenance_edit_gas_maintenance',
                       kwargs={'car_slug': self.car.slug,
                               'pk': self.pk})
    
    def get_delete_url(self):
        """
            Define a url object for deleting gasoline records. 
        """
        return reverse('auto_maintenance_delete_gas_maintenance',
                       kwargs={'car_slug': self.car.slug,
                               'pk': self.pk})


class OilChange(MaintenanceBase):
    """
        Oil Change instance of a maintenance record.  Just used to tag this
        record as the oil change.
    """

    def get_absolute_url(self):
        """
            Absolute URL for the detailed record.
        """
        return reverse('auto_oilchange_view_record',
                       kwargs={'car_slug': self.car.slug,
                               'pk': self.pk})
    
    def get_edit_url(self):
        """
            Define a url object for editing gasoline records.
        """
        return reverse('auto_maintenance_edit_oil_change',
                       kwargs={'car_slug': self.car.slug,
                               'pk': self.pk})
    
    def get_delete_url(self):
        """
            Define a url object for deleting gasoline records. 
        """
        return reverse('auto_maintenance_delete_oil_change',
                       kwargs={'car_slug': self.car.slug,
                               'pk': self.pk})

    def __unicode__(self):
        """
            Overrides the maintenance unicode string to show that the record
            was an oil change record.
        """
        return "Oil Change: %s" % self.date
    
    def human_readable_type(self):
        """ 
            Returns a human readable type information for this object type.
        """
        return "Oil Change"


class Maintenance(MaintenanceBase):
    """
        Other Maintenance record.
    """
    type = models.CharField(max_length=100)

    def __unicode__(self):
        """
            Overrides the mainentance unicode string to show that the record
            was for mainteance.
        """
        return "Maintenance (%s): %s" % (self.type, self.date)
    
    def human_readable_type(self):
        """ 
            Returns a human readable type information for this object type.
        """
        return self.type


class Payment(models.Model):
    """
        Collection of other payments that can be associated with a car
        purchase.  These can be taxes, parking, automobile associations,
        fines, tickets. Basically anything that doesn't have a mileage
        associated with it.
    """
    date = models.DateTimeField(unique=True, default=datetime.now)
    date_timezone = models.CharField(max_length=50, choices=timezone_choices,
                                     default=settings.TIME_ZONE)
    car = models.ForeignKey(Car)
    trip = models.ForeignKey(Trip, null=True, blank=True)
    location = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2,
                                     blank=True, default=0.0)
    type = models.CharField(max_length=11, choices=PAYMENT_TYPES,
                            default=DEFAULT_PAYMENT_TYPE)

    def get_absolute_url(self):
        """
            Absolute URL for the detailed record.
        """
        return reverse('auto_maintenance_view_payment',
                       kwargs={'car_slug': self.car.slug,
                               'pk': self.pk})

    def get_edit_url(self):
        """
            Define a url object for editing gasoline records.
        """
        return reverse('auto_maintenance_edit_payment',
                       kwargs={'car_slug': self.car.slug,
                               'pk': self.pk})

    def get_delete_url(self):
        """
            Define a url object for deleting gasoline records.
        """
        return reverse('auto_maintenance_delete_payment',
                       kwargs={'car_slug': self.car.slug,
                               'pk': self.pk})

    def human_readable_type(self):
        """
            Returns a human readable type information for this object type.
        """
        return self.get_type_display()