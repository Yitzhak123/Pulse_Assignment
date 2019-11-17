from django.urls import path
from . import views

urlpatterns = [
    path('', views.show_pulse_graph, name='show_pulse_graph'),
    path('tester_details_series_3', views.get_tester_details_of_series_3),
    path('count_testers_running_each_os', views.count_testers_running_each_os),
]
