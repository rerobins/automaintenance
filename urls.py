from django.contrib.auth.decorators import login_required
from django.conf.urls.defaults import *

from automaintenance.views import CarListView, CreateCarView, DisplayCar, CreateGasolinePurchase, MaintenanceView, EditMaintenanceView, DeleteMaintenanceView, EditGasolinePurchase, DeleteGasolinePurchase, CreateMaintenanceView, CreateOilChange, EditOilChange, DeleteOilChange, GasolinePurchaseView, OilChangeView, CreateTripView, DisplayTrip

urlpatterns = patterns('',
	url(r'^$',  login_required(CarListView.as_view())),
	
	# Car Records
        url(r'^add_car/$', login_required(CreateCarView.as_view()), name='auto_maintenance_add_car'),
        url(r'^(?P<slug>[^/]+)/$', login_required(DisplayCar.as_view()), name='auto_maintenance_car_detail'),

	# Gasoline Records
	url(r'^(?P<car_slug>[^/]+)/maintenance/gasoline/add/$', login_required(CreateGasolinePurchase.as_view()), name='auto_maintenance_create_gas_maintenance'),
	url(r'^(?P<car_slug>[^/]+)/maintenance/gasoline/(?P<slug>[^/]+)/edit/$', login_required(EditGasolinePurchase.as_view()), name='auto_maintenance_edit_gas_maintenance'),
	url(r'^(?P<car_slug>[^/]+)/maintenance/gasoline/(?P<slug>[^/]+)/delete/$', login_required(DeleteGasolinePurchase.as_view()), name='auto_maintenance_delete_gas_maintenance'),
	url(r'^(?P<car_slug>[^/]+)/maintenance/gasoline/(?P<slug>[^/]+)/$', login_required(GasolinePurchaseView.as_view()), name='auto_gasolinepurchase_view_record'),

	# Scheduled Maintenance Records
	url(r'^(?P<car_slug>[^/]+)/maintenance/scheduled/add/$', login_required(CreateMaintenanceView.as_view()), name='auto_maintenance_create_scheduled_maintenance'),
	url(r'^(?P<car_slug>[^/]+)/maintenance/scheduled/(?P<slug>[^/]+)/edit/$', login_required(EditMaintenanceView.as_view()), name='auto_maintenance_edit_scheduled_maintenance'),
	url(r'^(?P<car_slug>[^/]+)/maintenance/scheduled/(?P<slug>[^/]+)/delete/$', login_required(DeleteMaintenanceView.as_view()), name='auto_maintenance_delete_scheduled_maintenance'),
	url(r'^(?P<car_slug>[^/]+)/maintenance/scheduled/(?P<slug>[^/]+)/$', login_required(MaintenanceView.as_view()), name='auto_maintenance_view_record'),

	# Oil Change Records
	url(r'^(?P<car_slug>[^/]+)/maintenance/oilchange/add/$', login_required(CreateOilChange.as_view()), name='auto_maintenance_create_oil_change'),
	url(r'^(?P<car_slug>[^/]+)/maintenance/oilchange/(?P<slug>[^/]+)/edit/$', login_required(EditOilChange.as_view()), name='auto_maintenance_edit_oil_change'),
	url(r'^(?P<car_slug>[^/]+)/maintenance/oilchange/(?P<slug>[^/]+)/delete/$', login_required(DeleteOilChange.as_view()), name='auto_maintenance_delete_oil_change'),
	url(r'^(?P<car_slug>[^/]+)/maintenance/oilchange/(?P<slug>[^/]+)/$', login_required(OilChangeView.as_view()), name='auto_oilchange_view_record'),

	# Trip Records
	url(r'^(?P<car_slug>[^/]+)/trip/add/$', login_required(CreateTripView.as_view()), name="auto_maintenance_create_trip"),
	url(r'^(?P<car_slug>[^/]+)/trip/(?P<slug>[^/]+)/$', login_required(DisplayTrip.as_view()), name='auto_maintenance_trip_view'),
	
)
