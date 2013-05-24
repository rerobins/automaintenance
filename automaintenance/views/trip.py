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

from django.views.generic import CreateView, DetailView, UpdateView, DeleteView

from django.template.defaultfilters import slugify
from django.shortcuts import get_object_or_404

from automaintenance.models import Car, GasolinePurchase, OilChange
from automaintenance.models import Maintenance, Trip
from automaintenance.views.forms import TripForm
from automaintenance.views import MAINTENANCE_CRUD_BACK_KEY

from decimal import Decimal


class CreateTripView(CreateView):
    """
        Override CreateView to create new trip objects.
    """
    model = Trip
    form_class = TripForm

    def get(self, request, *args, **kwargs):
        """
            Override get to add a car field to the class object.
        """
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None), owner=self.request.user)
        self.initial['car'] = self.car
        return super(CreateTripView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
            Override the post field to add a car field to the class object.
        """
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None), owner=self.request.user)
        self.initial['car'] = self.car
        return super(CreateTripView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        """
            Override the form_valid method to make sure that the car that the
            record is defined for is stored in the object.
        """
        form.instance.car = self.car
        string = "%02d%02d%02d%s" % (form.instance.start.year, form.instance.start.month, form.instance.start.day,
                               form.instance.name)
        form.instance.slug = slugify(string)
        return super(CreateTripView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
            Adding some contextual data to the view including:
                maintenance list
        """
        context = super(CreateTripView, self).get_context_data(**kwargs)

        context['command'] = 'Add'
        context['car'] = self.car

        return context    

    
class EditTripView(UpdateView):   
    """
        Override the update view to edit trip items on a specific car.
    """
    model = Trip
    form_class = TripForm

    def form_valid(self, form):
        """
            Override the form_valid method to make sure that the car that the
            record is defined for is stored in the object.
        """
        form.instance.car = self.car
        return super(EditTripView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
            Add the command type to the maintenance view for display.
        """
        context = super(EditTripView, self).get_context_data(**kwargs)
        context['command'] = 'Edit'
        context['car'] = self.car
        return context

    def get_queryset(self):
        """
            When looking up the object to edit, make sure that the records are
            only found for the car that is defined in the url.
        """
        return self.model.objects.filter(car=self.car)

    def get_success_url(self):
        """
            Override the success url to go back to the car's detail page.
        """
        return self.object.get_absolute_url()

    def get(self, request, *args, **kwargs):
        """
            Override get to add a car field to the class object.
        """
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None),
            owner=request.user)
        return super(EditTripView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
            Override the post field to add a car field to the class object.
        """
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None),
            owner=request.user)
        return super(EditTripView, self).post(request, *args, **kwargs)        


class DisplayTripView(DetailView):
    """
        Override DetailView to show records associated with a trip object.
    """
    context_object_name = "trip"

    def get_queryset(self):
        """
            When looking up the object to edit, make sure that the trips are
            only found for the car that is defined in the url.
        """
        return Trip.objects.filter(car=self.car)

    def get(self, request, *args, **kwargs):
        """
            Override get to add a car field to the class object.
        """
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None), owner=self.request.user)

        return super(DisplayTripView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
            Adding some contextual data to the view including:
                maintenance list
        """
        context = super(DisplayTripView, self).get_context_data(**kwargs)

        gasoline_list = list(GasolinePurchase.objects.filter(trip=self.object))
        oilchange_list = list(OilChange.objects.filter(trip=self.object))
        maintenance_list = list(Maintenance.objects.filter(trip=self.object))

        maintenance_list = gasoline_list + oilchange_list + maintenance_list

        maintenance_list.sort()

        context['maintenance_list'] = maintenance_list
        
        total_price = Decimal(0.0)
        total_mileage = 0
        
        for maintenance in maintenance_list:
            total_price += maintenance.total_cost
            if hasattr(maintenance, 'tank_mileage'):
                total_mileage += maintenance.tank_mileage
                
        context['total_price'] = total_price
        context['total_mileage'] = total_mileage
        
        self.request.session[MAINTENANCE_CRUD_BACK_KEY] = self.object

        return context
    

class DeleteTripView(DeleteView):
    """
        Override the delete view to delete trip objects.
    """

    model = Trip

    def get(self, request, *args, **kwargs):
        """
            Override get to add a car field to the class object.
        """
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None),
            owner=request.user)

        return super(DeleteTripView, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(DeleteTripView, self).get_context_data(**kwargs)
        
        context['back_object'] = self.car
        if MAINTENANCE_CRUD_BACK_KEY in self.request.session:
            context['back_object']  = self.request.session[MAINTENANCE_CRUD_BACK_KEY]
        
        context['car'] = self.car
        
        return context

    def post(self, request, *args, **kwargs):
        """
            Override the post field to add a car field to the class object.
        """
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None),
            owner=request.user)
        return super(DeleteTripView, self).post(request, *args, **kwargs)

    def get_queryset(self):
        """
            When looking up the object to edit, make sure that the records are
            only found for the car that is defined in the url.
        """
        return self.model.objects.filter(car=self.car)

    def get_success_url(self):
        """
            Override the success url to go back to the car's detail page.
        """
        return_value = self.car.get_absolute_url()
        
        return return_value
