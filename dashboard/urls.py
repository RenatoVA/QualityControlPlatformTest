from django.urls import path
from .views import generate_daily_metrics, quality_trend, failure_distribution, best_worst_products

urlpatterns = [
    path('analytics/generate-daily-metrics/', generate_daily_metrics, name='generate_daily_metrics'),
    path('analytics/quality-trend/', quality_trend, name='quality_trend'),
    path('analytics/failure-distribution/', failure_distribution, name='failure_distribution'),
    path('analytics/best-worst-products/', best_worst_products, name='best_worst_products'),
]