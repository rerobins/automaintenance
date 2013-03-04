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
from automaintenance.models import Car

def car_list(request):
	if hasattr(request, 'user'):
		user = request.user
		if user.isAnonymous():
			car_list = []
		else:
			car_list = Car.objects.filter(owner=user)
	else:
		car_list = []

	return {
		'car_list': car_list,
	}

