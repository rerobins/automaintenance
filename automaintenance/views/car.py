##
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
from django.views.generic import ListView, CreateView, DetailView, UpdateView

from django.core.exceptions import ObjectDoesNotExist

from django.template.defaultfilters import slugify

from automaintenance.models import Car, GasolinePurchase, OilChange
from automaintenance.models import Trip
from automaintenance.views.forms import CarForm
from automaintenance.views import MAINTENANCE_CRUD_BACK_KEY
from datetime import date

from decimal import Decimal
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


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

        if self.queryset is None:
            self.queryset = Car.objects.filter(owner=self.request.user)

        return self.queryset

    def get(self, request, *args, **kwargs):
        return super(CarListView, self).get(request, *args, **kwargs)


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
    
    def get_context_data(self, **kwargs):
        """
            Add the command type to the car view for display.
        """
        context = super(CreateCarView, self).get_context_data(**kwargs)
        context['command'] = 'Add'
        return context

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
    

class EditCarView(UpdateView):   
    """
        Override the update view to edit trip items on a specific car.
    """
    model = Car
    form_class = CarForm

    def form_valid(self, form):
        """
            Override the form_valid method to make sure that the car that the
            record is defined for is stored in the object.
        """
        form.instance.owner = self.request.user
        form.instance.slug = slugify(form.instance.name)
        return super(EditCarView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
            Add the command type to the car view for display.
        """
        context = super(EditCarView, self).get_context_data(**kwargs)
        context['command'] = 'Edit'
        return context

    def get_queryset(self):
        """
            When looking up the object to edit, make sure that the records are
            only found for the car that is defined in the url.
        """
        return self.model.objects.filter(owner=self.request.user)

    def get_success_url(self):
        """
            Override the success url to go back to the car's detail page.
        """
        return self.object.get_absolute_url()        


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
        maintenance_list = self.object.get_maintenance_list()

        # Populate the last oil change for this car
        try:
            context['has_last_oil_change'] = True
            context['last_oil_change'] = OilChange.objects.filter(car=self.object).latest()
        except ObjectDoesNotExist:
            context['has_last_oil_change'] = False

        # Populate the last fill up for this car
        try:
            context['has_last_gas_purchase'] = True
            context['last_gas_purchase'] = GasolinePurchase.objects.filter(car=self.object).latest()
        except ObjectDoesNotExist:
            context['has_last_gas_purchase'] = False

        # Populate the tirp list for this car
        context['trip_list'] = Trip.objects.filter(car=self.object)
        
        # Calculate the total cost of maintaining the car
        total_cost = Decimal(0.0)
        ytd_cost = Decimal(0.0)
        ytd_mileage = Decimal(0.0)
        current_year = date.today().year
        
        for maintenance in maintenance_list:
            total_cost += maintenance.total_cost
            if maintenance.date.year == current_year:
                ytd_cost += maintenance.total_cost

            if hasattr(maintenance, 'tank_mileage'):
                ytd_mileage += maintenance.tank_mileage

        context['total_cost'] = total_cost
        context['ytd_cost'] = ytd_cost
        context['ytd_mileage'] = ytd_mileage
        context['ytd_cost_per_mile'] = ytd_cost / ytd_mileage
        
        self.request.session[MAINTENANCE_CRUD_BACK_KEY] = self.object

        paginator = Paginator(maintenance_list, 10) # Show 10 records per page

        page = self.request.GET.get('page')
        try:
            context['maintenance_list'] = paginator.page(page)
        except PageNotAnInteger:
            # If page is not an integer, deliver first page.
            context['maintenance_list'] = paginator.page(1)
        except EmptyPage:
            # If page is out of range (e.g. 9999), deliver last page of results.
            context['maintenance_list'] = paginator.page(paginator.num_pages)

        return context
