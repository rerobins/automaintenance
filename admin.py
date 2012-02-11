from django.contrib import admin

from automaintenance.models import CarType, Trip

class CarTypeAdmin(admin.ModelAdmin):
	pass

admin.site.register(CarType, CarTypeAdmin)

class TripAdmin(admin.ModelAdmin):
	pass

admin.site.register(Trip, TripAdmin)


