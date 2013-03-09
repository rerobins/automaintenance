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
from django.forms import ModelForm
from django.core.exceptions import ValidationError
from django.template.defaultfilters import slugify
from automaintenance.models import Car, GasolinePurchase, OilChange
from automaintenance.models import Maintenance, Trip


class CarForm(ModelForm):
    """
        Form that will allow for the adding of new cars to the database by a
        user.
    """

    def clean(self):
        """
            Overriden to validate the model before it is saved to the database,
            want to make sure that there are not two projects owned by the same
            user that have the same name.
        """
        cleaned_data = self.cleaned_data

        ## Make sure that there isn' already a project with the name requested
        ## owned by that user.
        try:
            Car.objects.get(slug=slugify(cleaned_data['name']),
                owner=self.initial['owner'])
        except:
            pass
        else:
            raise ValidationError("Car with this name already exists")

        return cleaned_data

    class Meta:
        """
            Define the meta data and the fields that are to be showed in this
            form.
        """

        model = Car

        fields = ('car_type',
                'name',)


class GasolinePurchaseForm(ModelForm):
    """
        Form that will allow for the definition of a gasoline purchase to be
        added to a specified car.
    """

    class Meta:
        """
            Define the meta data and the fields that are to be showed in this
            form.
        """
        model = GasolinePurchase

        fields = ('date',
                'location',
                'mileage',
                'description',
                'total_cost',
                'tank_mileage',
                'price_per_unit',
                'fuel_amount', 'trip')


class OilChangeForm(ModelForm):
    """
        Form that will allow for the definition of an oil change to be added
        to the specified car.
    """

    class Meta:
        """
            Define the meta data and the fields that are to be showed in this
            form.
        """
        model = OilChange

        fields = ('date',
                'location',
                'mileage',
                'description',
                'total_cost',
                'trip',
                )


class MaintenanceForm(ModelForm):
    """
        Form that will allow for a scheduled maintenance or any other
        maintenance to be added to the specified car.
    """

    class Meta:
        """
            Define the meta data and the fields that are to be showed in this
            form.
        """
        model = Maintenance

        fields = ('date',
                'location',
                'mileage',
                'description',
                'total_cost',
                'trip',
                )


class TripForm(ModelForm):
    """
        Form that will allow for a trip to be added in order to categorize
        maintenance data into trips that they should be associated with.
    """

    def clean(self):
        """
            Overriden to validate the model before it is saved to the database,
            want to make sure that there are not two projects owned by the same
            user that have the same name.
        """
        cleaned_data = self.cleaned_data

        ## Make sure that there isn' already a project with the name requested
        ## owned by that user.
        try:
            Trip.objects.get(slug=slugify(cleaned_data['name']),
                car=self.initial['car'])
        except:
            pass
        else:
            raise ValidationError("Car with this name already exists")

        return cleaned_data

    class Meta:
        """
            Define the meta data and the fields that are to be showed in this
            form.
        """
        model = Trip

        fields = ('name', 'description', 'start', 'end')
