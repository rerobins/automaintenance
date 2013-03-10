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
from django.views.generic import DeleteView

from django.http import HttpResponseRedirect
from django.template.defaultfilters import slugify
from django.shortcuts import get_object_or_404

from automaintenance.models import Car, GasolinePurchase, OilChange
from automaintenance.models import Maintenance, Trip
from automaintenance.forms import CarForm, GasolinePurchaseForm, OilChangeForm
from automaintenance.forms import MaintenanceForm, TripForm


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
    model = Car

    form_class = CarForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.owner = self.request.user
        self.object.slug = slugify(self.object.name)

        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

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
        self.user = request.user
        self.initial['owner'] = request.user
        return super(CreateCarView, self).post(request, *args, **kwargs)


class DisplayCar(DetailView):

    context_object_name = "car"

    def get_queryset(self):
        return Car.objects.filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        # Populate the maintenance list for this car
        gasoline_list = list(GasolinePurchase.objects.filter(car=self.object))
        oilchange_list = list(OilChange.objects.filter(car=self.object))
        maintenance_list = list(Maintenance.objects.filter(car=self.object))
        maintenance_list = gasoline_list + oilchange_list + maintenance_list
        maintenance_list.sort()
        context['maintenance_list'] = maintenance_list

        # Populate the tirp list for this car
        context['trip_list'] = Trip.objects.filter(car=self.object)

        return context


class MaintenanceView(DetailView):

    context_object_name = "car"

    def get(self, request, *args, **kwargs):
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None),
            owner=self.request.user)

        return super(DetailView, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return Maintenance.objects.filter(car=self.car)


class CreateMaintenanceView(CreateView):

    model = Maintenance
    form_class = MaintenanceForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.car = self.car
        self.object.save()

        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(CreateView, self).get_context_data(**kwargs)
        context['command'] = 'Add'
        return context

    def get_success_url(self):
        """
            Override the success url to go back to the car's detail page.
        """
        return self.car.get_absolute_url()

    def get(self, request, *args, **kwargs):
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None),
            owner=request.user)

        return super(CreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None),
            owner=request.user)
        return super(CreateView, self).post(request, *args, **kwargs)


class EditMaintenanceView(UpdateView):
    model = Maintenance
    form_class = MaintenanceForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.car = self.car
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, **kwargs):
        context = super(UpdateView, self).get_context_data(**kwargs)
        context['command'] = 'Update'
        return context

    def get_success_url(self):
        """
            Override the success url to go back to the car's detail page.
        """
        return self.car.get_absolute_url()

    def get(self, request, *args, **kwargs):
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None),
            owner=request.user)
        return super(UpdateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None),
            owner=request.user)
        return super(UpdateView, self).post(request, *args, **kwargs)


class DeleteMaintenanceView(DeleteView):

    model = Maintenance

    def get(self, request, *args, **kwargs):
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None),
            owner=request.user)

        return super(DeleteView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None),
            owner=request.user)
        self.success_url = self.car.get_absolute_url()
        return super(DeleteView, self).post(request, *args, **kwargs)

    def get_success_url(self):
        """
            Override the success url to go back to the car's detail page.
        """
        return self.car.get_absolute_url()


class CreateGasolinePurchase(CreateMaintenanceView):
    model = GasolinePurchase
    form_class = GasolinePurchaseForm


class EditGasolinePurchase(EditMaintenanceView):
    model = GasolinePurchase
    form_class = GasolinePurchaseForm


class DeleteGasolinePurchase(DeleteMaintenanceView):
    model = GasolinePurchase


class CreateOilChange(CreateMaintenanceView):
    model = OilChange
    form_class = OilChangeForm


class EditOilChange(EditMaintenanceView):
    model = OilChange
    form_class = OilChangeForm


class DeleteOilChange(CreateMaintenanceView):
    model = OilChange


class OilChangeView(MaintenanceView):
    def get_queryset(self):
        return OilChange.objects.filter(car=self.car)


class GasolinePurchaseView(MaintenanceView):

    def get_queryset(self):
        return GasolinePurchase.objects.filter(car=self.car)


class CreateTripView(CreateView):
    model = Trip

    form_class = TripForm

    def get(self, request, *args, **kwargs):
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None), owner=self.request.user)
        self.initial['car'] = self.car
        return super(CreateView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None), owner=self.request.user)
        self.initial['car'] = self.car
        return super(CreateView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.car = self.car
        self.object.slug = slugify(self.object.name)

        self.object.save()

        return HttpResponseRedirect(self.get_success_url())


class DisplayTrip(DetailView):

    context_object_name = "trip"

    def get_queryset(self):
        return Trip.objects.filter(car=self.car)

    def get(self, request, *args, **kwargs):
        self.car = get_object_or_404(Car,
            slug=self.kwargs.get('car_slug', None), owner=self.request.user)

        return super(DetailView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)

        gasoline_list = list(GasolinePurchase.objects.filter(trip=self.object))
        oilchange_list = list(OilChange.objects.filter(trip=self.object))
        maintenance_list = list(Maintenance.objects.filter(trip=self.object))

        maintenance_list = gasoline_list + oilchange_list + maintenance_list

        maintenance_list.sort()

        context['maintenance_list'] = maintenance_list

        return context
