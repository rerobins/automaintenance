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
from django.contrib.auth.decorators import login_required
from django.conf.urls import url, patterns

from automaintenance.views.car import CarListView, CreateCarView, DisplayCar, EditCarView
from automaintenance.views.maintenance import CreateGasolinePurchase, MaintenanceView
from automaintenance.views.maintenance import EditMaintenanceView, DeleteMaintenanceView
from automaintenance.views.maintenance import EditGasolinePurchase, DeleteGasolinePurchase
from automaintenance.views.maintenance import CreateMaintenanceView, CreateOilChange
from automaintenance.views.maintenance import EditOilChange, DeleteOilChange
from automaintenance.views.maintenance import GasolinePurchaseView, OilChangeView
from automaintenance.views.trip import CreateTripView, DisplayTripView, EditTripView
from automaintenance.views.trip import DeleteTripView
from automaintenance.views.report import DistancePerUnitReport, CostPerDistanceReport
from automaintenance.views.report import PricePerUnitReport, CategoryReport

urlpatterns = patterns('',
    url(r'^$', login_required(CarListView.as_view()),
        name='auto_maintenance_car_list'),

    # Car Records
    url(r'^add_car/$',
        login_required(CreateCarView.as_view()),
        name='auto_maintenance_add_car'),
    url(r'^car/(?P<slug>[^/]+)/$',
        login_required(DisplayCar.as_view()),
        name='auto_maintenance_car_detail'),
    url(r'^car/(?P<slug>[^/]+)/edit/$',
        login_required(EditCarView.as_view()),
        name='auto_maintenance_edit_car'),

    # Gasoline Records
    url(r'^car/(?P<car_slug>[^/]+)/maintenance/gasoline/add/$',
        login_required(CreateGasolinePurchase.as_view()),
        name='auto_maintenance_create_gas_maintenance'),
    url(r'^car/(?P<car_slug>[^/]+)/gasoline/(?P<pk>\d+)/edit/$',
        login_required(EditGasolinePurchase.as_view()),
        name='auto_maintenance_edit_gas_maintenance'),
    url(r'^car/(?P<car_slug>[^/]+)/gasoline/(?P<pk>\d+)/delete/$',
        login_required(DeleteGasolinePurchase.as_view()),
        name='auto_maintenance_delete_gas_maintenance'),
    url(r'^car/(?P<car_slug>[^/]+)/gasoline/(?P<pk>\d+)/$',
        login_required(GasolinePurchaseView.as_view()),
        name='auto_gasolinepurchase_view_record'),

    # Scheduled Maintenance Records
    url(r'^car/(?P<car_slug>[^/]+)/scheduled/add/$',
        login_required(CreateMaintenanceView.as_view()),
        name='auto_maintenance_create_scheduled_maintenance'),
    url(r'^car/(?P<car_slug>[^/]+)/scheduled/(?P<pk>\d+)/edit/$',
        login_required(EditMaintenanceView.as_view()),
        name='auto_maintenance_edit_scheduled_maintenance'),
    url(r'^car/(?P<car_slug>[^/]+)/scheduled/(?P<pk>\d+)/delete/$',
        login_required(DeleteMaintenanceView.as_view()),
        name='auto_maintenance_delete_scheduled_maintenance'),
    url(r'^car/(?P<car_slug>[^/]+)/scheduled/(?P<pk>\d+)/$',
        login_required(MaintenanceView.as_view()),
        name='auto_maintenance_view_record'),

    # Oil Change Records
    url(r'^car/(?P<car_slug>[^/]+)/oilchange/add/$',
        login_required(CreateOilChange.as_view()),
        name='auto_maintenance_create_oil_change'),
    url(r'^car/(?P<car_slug>[^/]+)/oilchange/(?P<pk>\d+)/edit/$',
        login_required(EditOilChange.as_view()),
        name='auto_maintenance_edit_oil_change'),
    url(r'^car/(?P<car_slug>[^/]+)/oilchange/(?P<pk>\d+)/delete/$',
        login_required(DeleteOilChange.as_view()),
        name='auto_maintenance_delete_oil_change'),
    url(r'^car/(?P<car_slug>[^/]+)/oilchange/(?P<pk>\d+)/$',
        login_required(OilChangeView.as_view()),
        name='auto_oilchange_view_record'),

    # Trip Records
    url(r'^car/(?P<car_slug>[^/]+)/trip/add/$',
        login_required(CreateTripView.as_view()),
        name="auto_maintenance_create_trip"),
    url(r'^car/(?P<car_slug>[^/]+)/trip/(?P<slug>[^/]+)/$',
        login_required(DisplayTripView.as_view()),
        name='auto_maintenance_trip_view'),
    url(r'^car/(?P<car_slug>[^/]+)/trip/(?P<slug>[^/]+)/edit/$',
        login_required(EditTripView.as_view()),
        name='auto_maintenance_edit_trip'),
    url(r'^car/(?P<car_slug>[^/]+)/trip/(?P<slug>[^/]+)/delete/$',
        login_required(DeleteTripView.as_view()),
        name='auto_maintenance_delete_trip'),
                       
    # Reports
    url(r'^car/(?P<car_slug>[^/]+)/reports/mpg/$',
        login_required(DistancePerUnitReport.as_view()),
        name='auto_maintenance_distance_per_unit'),
    url(r'^car/(?P<car_slug>[^/]+)/reports/cpm/$',
        login_required(CostPerDistanceReport.as_view()),
        name='auto_maintenance_cost_per_distance'),
    url(r'^car/(?P<car_slug>[^/]+)/reports/ppg/$',
        login_required(CostPerDistanceReport.as_view()),
        name='auto_maintenance_price_per_gallon'),
    url(r'^car/(?P<car_slug>[^/]+)/reports/category_expense/$',
        login_required(CategoryReport.as_view()),
        name='auto_maintenance_category_expense'),

)
