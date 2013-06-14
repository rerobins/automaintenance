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
    
    def convert_dates(self):
        """
            Converts the get parameters into date values.
        """
        end_date = datetime.now()
        if 'end_date' in self.request.GET:  
            end_date_string = self.request.GET['end_date']             
            end_date = datetime.combine(parse_date(end_date_string), time(0))
            
        start_date = end_date - timedelta(weeks=4)
        if 'start_date' in self.request.GET:
            start_date_string = self.request.GET['start_date']
            start_date = datetime.combine(parse_date(start_date_string), time(0))
        
        self.start_date = make_aware(start_date, get_default_timezone())
        self.end_date = make_aware(end_date, get_default_timezone())
        
    def get_car(self, car_slug):
        """
            Get the car value based on the provided slug.
        """
        self.car = Car.objects.get(owner=self.request.user, slug=car_slug)
        return self.car
        
    def get_records(self):
        """
            Filter down the records for the car so that they 
        """
        self.records = self.car.maintenance_query(GasolinePurchase, self.start_date, self.end_date)
        
        return self.records
    
    def get_context_data(self, **kwargs):
        """
            Override the context data with the values.
        """
        context = super(ReportView, self).get_context_data(**kwargs)
        
        self.get_car(kwargs['car_slug'])
        self.convert_dates()
        self.get_records()
        
        context['maintenance_list'] = self.records 
        context['start_date'] = self.start_date
        context['end_date'] = self.end_date
        context['car'] = self.car
        
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
    

class CategoryReport(ReportView):


    """
        Report that will provide functionality to show how money is spent across the 
        types of expenses.
    """
    template_name = "automaintenance/report/category_price.html"
    
    def get_records(self):
        """
            Filter down the records for the car so that they 
        """
        self.records = self.car.get_maintenance_list(self.start_date, self.end_date)
        
        return self.records
    
    def get_context_data(self, **kwargs):
        """
            Override the context data with the values.
        """
        context = super(CategoryReport, self).get_context_data(**kwargs)
        
        categories = {}
        
        for record in self.records:
            if record.human_readable_type() not in categories:
                categories[record.human_readable_type()] = record.total_cost
            else:
                categories[record.human_readable_type()] += record.total_cost
                
        context['categories'] = categories
        
        return context
        

class DistancePerTime(ReportView):
    """
        Report that tracks the total mileage of a car and the miles that are entered per 
        gasoline record.
    """
    template_name = "automaintenance/report/distance_per_time.html"