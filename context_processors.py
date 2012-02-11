from automaintenance.models import Car

def car_list(request):
	if hasattr(request, 'user'):
		user = request.user
		if user.is_anonymous():
			car_list = []
		else:
			car_list = Car.objects.filter(owner=user)
	else:
		car_list = []

	return {
		'car_list': car_list,
	}

