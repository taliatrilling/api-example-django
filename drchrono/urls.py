from django.conf.urls import include, url
from django.views.generic import TemplateView
from django.contrib import admin

import views


urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name='index.html'), name='home'),

    url(r'reminder', views.reminder, name='reminder'),

    url(r'', include('social.apps.django_app.urls', namespace='social')),
]
