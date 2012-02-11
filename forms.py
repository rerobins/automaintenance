from django.forms import ModelForm
from automaintenance.models import Car, GasolinePurchase, OilChange, ScheduledMaintenance, Trip

class CarForm(ModelForm):
	class Meta:
		model = Car

		fields = ('car_type', 
				'name', 
				'starting_mileage', 
				'purchase_date' )

class GasolinePurchaseForm(ModelForm):
	class Meta:
		model = GasolinePurchase

		fields = ('date', 
				'location', 
				'mileage', 
				'description', 
				'total_cost', 
				'tank_mileage', 
				'price_per_gallon', 
				'gallons', 'trip')

class OilChangeForm(ModelForm):
	class Meta:
		model = OilChange

		fields = ('date', 
				'location', 
				'mileage', 
				'description', 
				'total_cost', 
                                'trip',
				)

class ScheduledMaintenanceForm(ModelForm):
	class Meta:
		model = ScheduledMaintenance

		fields = ('date', 
				'location', 
				'mileage', 
				'description', 
				'total_cost', 
                                'trip',
				)

class TripForm(ModelForm):
	class Meta:
		model = Trip

		fields = ('name', 'description', 'start', 'end')


