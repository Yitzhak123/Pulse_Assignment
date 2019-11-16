from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_pulse_graph, name='show_pulse_graph'),
]
