from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QualityTestViewSet, QualityRuleViewSet, QualityCheckCreateView, QualityHistoryListView

router = DefaultRouter()
router.register(r'quality-tests', QualityTestViewSet)
router.register(r'quality-rules', QualityRuleViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('quality-checks/', QualityCheckCreateView.as_view(), name="quality-check-create"),
    path('quality-history/', QualityHistoryListView.as_view(), name="quality-history-list"),
]
