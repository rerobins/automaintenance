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

from django.views.generic.base import TemplateView

from automaintenance.models import GasolinePurchase, Car

from django.utils.timezone import make_aware, get_default_timezone
from django.utils.dateparse import parse_date

from datetime import datetime, time, timedelta

class ReportView(TemplateView):
    """
        Default report view.
    """
    
    template_name = "automaintenance/report.html"
    
    def get_context_data(self, **kwargs):
        context = super(ReportView, self).get_context_data(**kwargs)
        
        car = Car.objects.get(slug=kwargs['car_slug'])
        
        end_date = datetime.now()
        if 'end_date' in self.request.GET:  
            end_date_string = self.request.GET['end_date']             
            end_date = datetime.combine(parse_date(end_date_string), time(0))
            
        start_date = end_date - timedelta(weeks=4)
        if 'start_date' in self.request.GET:
            start_date_string = self.request.GET['start_date']
            start_date = datetime.combine(parse_date(start_date_string), time(0))
        
        start_date = make_aware(start_date, get_default_timezone())
        end_date = make_aware(end_date, get_default_timezone())
        
        records = GasolinePurchase.objects.filter(car=car).filter(date__gte=start_date).filter(date__lte=end_date)
        
        context['maintenance_list'] = records 
        context['start_date'] = start_date
        context['end_date'] = end_date
        context['car'] = car
        
        return context
    

class DistancePerUnitReport(ReportView):
    """
        Distance per unit report.
    """
    template_name = "automaintenance/report/distance_per_unit.html"
    

class CostPerDistanceReport(ReportView):
    """
        Cost per distance report.
    """
    template_name = "automaintenance/report/cost_per_distance.html"
    

class PricePerUnitReport(ReportView):
    """
        Price per unit report.
    """
    template_name = "automaintenance/report/price_per_unit.html"
    