from django.urls import path
from .views import get_satellite_stats, get_satellite_health

urlpatterns = [
    path('stats/', get_satellite_stats, name='satellite-stats'),
    path('health/', get_satellite_health, name='satellite-health'),
]
