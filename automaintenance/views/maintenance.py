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

from django.views.generic import CreateView, DetailView, UpdateView
from django.views.generic import DeleteView

from django.template.defaultfilters import slugify
from django.shortcuts import get_object_or_404

from automaintenance.models import Car, GasolinePurchase, OilChange
from automaintenance.models import Maintenance, Trip
from automaintenance.views.forms import GasolinePurchaseForm, OilChangeForm
from automaintenance.views.forms import MaintenanceForm, TripForm
from automaintenance.views import MAINTENANCE_CRUD_BACK_KEY

from decimal import Decimal

class MaintenanceView(DetailView):
    """
        Base view for the maintenance record display.
    """
    context_object_name = 'record'
    model = Maintenance

    def get(self, request, *args, **kwargs):
        """
            Adds a class variable pointing the car that the maintenance record
            is supposed to be related to.
        """
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None),
            owner=self.request.user)

        return super(DetailView, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(MaintenanceView, self).get_context_data(**kwargs)
        
        return_value = self.car.get_absolute_url()
        if MAINTENANCE_CRUD_BACK_KEY in self.request.session:
            return_value = self.request.session[MAINTENANCE_CRUD_BACK_KEY].get_absolute_url()
            del self.request.session[MAINTENANCE_CRUD_BACK_KEY]
        context['back_url'] = return_value
        
        return context

    def get_queryset(self):
        """
            Queryset override that makes sure that the record that is searched
            for belongs to the car defined in the url.
        """
        return self.model.objects.filter(car=self.car)


class CreateMaintenanceView(CreateView):
    """
        View that will allow for the creation of new maintenance records.  This
        class can be used as a base class for the creation of all maintenance
        records.
    """
    model = Maintenance
    form_class = MaintenanceForm

    def form_valid(self, form):
        """
            Make sure that the car value is stored in the model object before
            it is saved.
        """
        form.instance.car = self.car
        return super(CreateMaintenanceView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['command'] = 'Add'
        return context

    def get_success_url(self):
        """
            Override the success url to go back to the car's detail page.
        """
        return_value = self.car.get_absolute_url()
        if MAINTENANCE_CRUD_BACK_KEY in self.request.session:
            return_value = self.request.session[MAINTENANCE_CRUD_BACK_KEY].get_absolute_url()
            del self.request.session[MAINTENANCE_CRUD_BACK_KEY]
        
        return return_value

    def get(self, request, *args, **kwargs):
        """
            Override get to add a car field to the class object.
        """
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None),
            owner=request.user)

        return super(CreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
            Override the post field to add a car field to the class object.
        """
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None),
            owner=request.user)
        return super(CreateView, self).post(request, *args, **kwargs)

    def get_form(self, form_class):
        """
            Returns an instance of the form to be used in this view.  Overriden
            to limit the trips that are going to be used to the ones that
            are allowed in the currently edited car.
        """
        form = super(CreateMaintenanceView, self).get_form(form_class)

        form.fields['trip'].queryset = Trip.objects.filter(
            car=self.car)

        return form


class EditMaintenanceView(UpdateView):
    """
        Override the update view to edit maintenance items on a specific car.
    """
    model = Maintenance
    form_class = MaintenanceForm

    def form_valid(self, form):
        """
            Override the form_valid method to make sure that the car that the
            record is defined for is stored in the object.
        """
        form.instance.car = self.car
        return super(EditMaintenanceView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
            Add the command type to the maintenance view for display.
        """
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['command'] = 'Update'
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
        return_value = self.car.get_absolute_url()
        if MAINTENANCE_CRUD_BACK_KEY in self.request.session:
            return_value = self.request.session[MAINTENANCE_CRUD_BACK_KEY].get_absolute_url()
            del self.request.session[MAINTENANCE_CRUD_BACK_KEY]
        
        return return_value

    def get(self, request, *args, **kwargs):
        """
            Override get to add a car field to the class object.
        """
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None),
            owner=request.user)
        return super(UpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
            Override the post field to add a car field to the class object.
        """
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None),
            owner=request.user)
        return super(UpdateView, self).post(request, *args, **kwargs)


class DeleteMaintenanceView(DeleteView):
    """
        Override the delete view to delete maintenance objects.
    """

    model = Maintenance

    def get(self, request, *args, **kwargs):
        """
            Override get to add a car field to the class object.
        """
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None),
            owner=request.user)

        return super(DeleteView, self).get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super(DeleteView, self).get_context_data(**kwargs)
        
        context['back_object'] = self.car
        if MAINTENANCE_CRUD_BACK_KEY in self.request.session:
            context['back_object']  = self.request.session[MAINTENANCE_CRUD_BACK_KEY]
        
        return context

    def post(self, request, *args, **kwargs):
        """
            Override the post field to add a car field to the class object.
        """
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None),
            owner=request.user)
        return super(DeleteView, self).post(request, *args, **kwargs)

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
        if MAINTENANCE_CRUD_BACK_KEY in self.request.session:
            return_value = self.request.session[MAINTENANCE_CRUD_BACK_KEY].get_absolute_url()
            del self.request.session[MAINTENANCE_CRUD_BACK_KEY]
        
        return return_value
    

class CreateGasolinePurchase(CreateMaintenanceView):
    """
        Override the CreateMaintenanceView to create gasoline purchases.
    """
    model = GasolinePurchase
    form_class = GasolinePurchaseForm


class EditGasolinePurchase(EditMaintenanceView):
    """
        Override the EditMaintenanceView to edit gasoline purchases.
    """
    model = GasolinePurchase
    form_class = GasolinePurchaseForm


class DeleteGasolinePurchase(DeleteMaintenanceView):
    """
        Override the DeleteMaintenanceView to delete gasoline purchases.
    """
    model = GasolinePurchase


class CreateOilChange(CreateMaintenanceView):
    """
        Override the CreateMaintenanceView to create oil changes.
    """
    model = OilChange
    form_class = OilChangeForm


class EditOilChange(EditMaintenanceView):
    """
        Override the EditMaintenanceView to edit oil changes.
    """
    model = OilChange
    form_class = OilChangeForm


class DeleteOilChange(DeleteMaintenanceView):
    """
        Override the DeleteMaintenanceView to delete oil changes.
    """
    model = OilChange


class OilChangeView(MaintenanceView):
    """
        Override the MaintenanceView to show oil changes.
    """
    model = OilChange


class GasolinePurchaseView(MaintenanceView):
    """
        Override the MaintenanceView to show gasoline purchases.
    """
    model = GasolinePurchase


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


class DisplayTrip(DetailView):
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

        return super(DetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        """
            Adding some contextual data to the view including:
                maintenance list
        """
        context = super(DetailView, self).get_context_data(**kwargs)

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

        return context
