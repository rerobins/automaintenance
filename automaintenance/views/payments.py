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

from django.shortcuts import get_object_or_404

from automaintenance.models import Car
from automaintenance.models import Trip, Payment
from automaintenance.views.forms import PaymentForm
from automaintenance.views import MAINTENANCE_CRUD_BACK_KEY


class PaymentView(DetailView):
    """
        Base view for the maintenance record display.
    """
    context_object_name = 'payment'
    model = Payment

    def get(self, request, *args, **kwargs):
        """
            Adds a class variable pointing the car that the maintenance record
            is supposed to be related to.
        """
        self.car = get_object_or_404(Car,
                                     slug=self.kwargs.get('car_slug', None),
                                     owner=self.request.user)

        return super(PaymentView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(PaymentView, self).get_context_data(**kwargs)

        context['back_object'] = self.car
        if MAINTENANCE_CRUD_BACK_KEY in self.request.session:
            context['back_object'] = self.request.session[MAINTENANCE_CRUD_BACK_KEY]
        context['car'] = self.car

        return context

    def get_queryset(self):
        """
            Queryset override that makes sure that the record that is searched
            for belongs to the car defined in the url.
        """
        return self.model.objects.filter(car=self.car)


class CreatePaymentView(CreateView):
    """
        View that will allow for the creation of new maintenance records.  This
        class can be used as a base class for the creation of all maintenance
        records.
    """
    model = Payment
    form_class = PaymentForm

    def form_valid(self, form):
        """
            Make sure that the car value is stored in the model object before
            it is saved.
        """
        form.instance.car = self.car
        return super(CreatePaymentView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreatePaymentView, self).get_context_data(**kwargs)
        context['command'] = 'Add'
        context['car'] = self.car

        context['back_object'] = self.car
        if MAINTENANCE_CRUD_BACK_KEY in self.request.session:
            context['back_object']  = self.request.session[MAINTENANCE_CRUD_BACK_KEY]

        return context

    def get_success_url(self):
        """
            Override the success url to go back to the car's detail page.
        """
        return_value = self.car.get_absolute_url()
        if MAINTENANCE_CRUD_BACK_KEY in self.request.session:
            return_value = self.request.session[MAINTENANCE_CRUD_BACK_KEY].get_absolute_url()

        return return_value

    def get(self, request, *args, **kwargs):
        """
            Override get to add a car field to the class object.
        """
        self.car = get_object_or_404(Car,
                                     slug=self.kwargs.get('car_slug', None),
                                     owner=request.user)

        return super(CreatePaymentView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
            Override the post field to add a car field to the class object.
        """
        self.car = get_object_or_404(Car,
                                     slug=self.kwargs.get('car_slug', None),
                                     owner=request.user)

        return super(CreatePaymentView, self).post(request, *args, **kwargs)

    def get_form(self, form_class):
        """
            Returns an instance of the form to be used in this view.  Overridden
            to limit the trips that are going to be used to the ones that
            are allowed in the currently edited car.
        """
        form = super(CreatePaymentView, self).get_form(form_class)

        form.fields['trip'].queryset = Trip.objects.filter(
            car=self.car)

        return form


class EditPaymentView(UpdateView):
    """
        Override the update view to edit maintenance items on a specific car.
    """
    model = Payment
    form_class = PaymentForm

    def form_valid(self, form):
        """
            Override the form_valid method to make sure that the car that the
            record is defined for is stored in the object.
        """
        form.instance.car = self.car
        return super(EditPaymentView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        """
            Add the command type to the maintenance view for display.
        """
        context = super(EditPaymentView, self).get_context_data(**kwargs)
        context['command'] = 'Update'
        context['car'] = self.car

        context['back_object'] = self.car
        if MAINTENANCE_CRUD_BACK_KEY in self.request.session:
            context['back_object']  = self.request.session[MAINTENANCE_CRUD_BACK_KEY]

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

        return return_value

    def get(self, request, *args, **kwargs):
        """
            Override get to add a car field to the class object.
        """
        self.car = get_object_or_404(Car,
                                     slug=self.kwargs.get('car_slug', None),
                                     owner=request.user)
        return super(EditPaymentView, self).get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        """
            Override the post field to add a car field to the class object.
        """
        self.car = get_object_or_404(Car,
                                     slug=self.kwargs.get('car_slug', None),
                                     owner=request.user)
        return super(EditPaymentView, self).post(request, *args, **kwargs)


class DeletePaymentView(DeleteView):
    """
        Override the delete view to delete maintenance objects.
    """

    model = Payment

    def get(self, request, *args, **kwargs):
        """
            Override get to add a car field to the class object.
        """
        self.car = get_object_or_404(Car,
                                     slug=self.kwargs.get('car_slug', None),
                                     owner=request.user)

        return super(DeletePaymentView, self).get(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super(DeleteView, self).get_context_data(**kwargs)

        context['back_object'] = self.car
        if MAINTENANCE_CRUD_BACK_KEY in self.request.session:
            context['back_object'] = self.request.session[MAINTENANCE_CRUD_BACK_KEY]

        context['car'] = self.car

        return context

    def post(self, request, *args, **kwargs):
        """
            Override the post field to add a car field to the class object.
        """
        self.car = get_object_or_404(Car,
                                     slug=self.kwargs.get('car_slug', None),
                                     owner=request.user)
        return super(DeletePaymentView, self).post(request, *args, **kwargs)

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
