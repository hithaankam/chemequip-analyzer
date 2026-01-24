from django.urls import path
from .views import EquipmentAnalysisView

urlpatterns = [
    path('analyze/', EquipmentAnalysisView.as_view(), name='equipment-analysis'),
]