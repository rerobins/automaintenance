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
from django.views.generic import ListView, CreateView, DetailView

from django.core.exceptions import ObjectDoesNotExist

from django.template.defaultfilters import slugify

from automaintenance.models import Car, GasolinePurchase, OilChange
from automaintenance.models import Maintenance, Trip
from automaintenance.views.forms import CarForm

class CarListView(ListView):
    """
        Return the list of cars that are owned by the user that is posting the
        requests.
    """
    context_object_name = "car_list"
    model = Car

    def get_queryset(self):
        """
            Trim down the query result automatically by the owner of the car.
        """
        return Car.objects.filter(owner=self.request.user)


class CreateCarView(CreateView):
    """
        View that creates a new car.
    """
    model = Car
    form_class = CarForm

    def form_valid(self, form):
        """
            Create the slug for the car and assign the owner to the car before
            saving it.
        """
        form.instance.owner = self.request.user
        form.instance.slug = slugify(form.instance.name)
        return super(CreateCarView, self).form_valid(form)

    def get(self, request, *args, **kwargs):
        """
            Override the get so that the initial object's owner can be set to
            the request user.
        """
        self.initial['owner'] = request.user
        return super(CreateCarView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
            Override the post so that the initial object's owner can be set to
            the request user.
        """
        self.initial['owner'] = request.user
        return super(CreateCarView, self).post(request, *args, **kwargs)


class DisplayCar(DetailView):
    """
        The view that is responsible for showing off all of the details of the
        car, including the records that make up the maintenance values of the
        car.
    """
    context_object_name = "car"

    def get_queryset(self):
        """
            Override the queryset used to look up the object so that it only
            returns the cars that are owned by the requests user.
        """
        return Car.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        """
            Adding some contextual data to the view including:
                maintenance list
                the last oil change
                the last gasoline purchase
        """
        context = super(DetailView, self).get_context_data(**kwargs)

        # Populate the maintenance list for this car
        gasoline_list = list(GasolinePurchase.objects.filter(car=self.object))
        oilchange_list = list(OilChange.objects.filter(car=self.object))
        maintenance_list = list(Maintenance.objects.filter(car=self.object))
        maintenance_list = gasoline_list + oilchange_list + maintenance_list
        maintenance_list.sort()
        context['maintenance_list'] = maintenance_list

        # Populate the last oil change for this car
        try:
            context['has_last_oil_change'] = True
            context['last_oil_change'] = OilChange.objects.filter(
                    car=self.object).latest()
        except ObjectDoesNotExist:
            context['has_last_oil_change'] = False

        # Populate the last fill up for this car
        try:
            context['has_last_gas_purchase'] = True
            context['last_gas_purchase'] = GasolinePurchase.objects.filter(
                    car=self.object).latest()
        except ObjectDoesNotExist:
            context['has_last_gas_purchase'] = False

        # Populate the tirp list for this car
        context['trip_list'] = Trip.objects.filter(car=self.object)
        
        self.request.session['maintenance_add_back'] = self.object

        return context
