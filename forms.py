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


