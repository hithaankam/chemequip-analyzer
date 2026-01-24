from django.urls import path
from .views import EquipmentAnalysisView, DatasetHistoryView, DatasetDetailView, AuthLoginView, AuthRegisterView

urlpatterns = [
    path('analyze/', EquipmentAnalysisView.as_view(), name='equipment-analysis'),
    path('history/', DatasetHistoryView.as_view(), name='dataset-history'),
    path('dataset/<int:dataset_id>/', DatasetDetailView.as_view(), name='dataset-detail'),
    path('login/', AuthLoginView.as_view(), name='auth-login'),
    path('register/', AuthRegisterView.as_view(), name='auth-register'),
]