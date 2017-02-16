from django.views.generic.base import TemplateView

from django.template import Context

from datetime import datetime

from social.apps.django_app.default.models import UserSocialAuth

from django.shortcuts import render

import requests


def reminder(request):
	"""Page with reminders of patient birthdays, including error handling if user navigates to
	without authorizing/logging in"""

	user = request.user
	try:
		drchrono_login = user.social_auth.get(provider='drchrono')
	except UserSocialAuth.DoesNotExist:
		drchrono_login = None
	except AttributeError:
		drchrono_login = None
	if drchrono_login is not None:
		access_token_auth = 'Bearer ' + str(drchrono_login.access_token)
		headers = {
	    'Authorization': access_token_auth
	}
		bdays = []
		today = datetime.now().strftime('%m-%d')
		patients_url = 'https://drchrono.com/api/patients_summary'
		data = requests.get(patients_url, headers=headers)
		d = data.json()
		for entry in d['results']:
		    if str(entry['date_of_birth']).endswith(today):
		        bdays.append((str(entry['first_name']) + ' ' + str(entry['last_name'])))
		context = {'bdays': bdays, 'drchrono_login': drchrono_login}
		return render(request, 'reminder.html', context)
	return render(request, 'reminder.html')




