from django.db.models import Count
from django.utils.timezone import now
from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.db import models
from .models import QualityTest, QualityMetricHistory

@api_view(['POST'])
def generate_daily_metrics(request):
    """Procesa las pruebas de calidad del día y almacena métricas históricas."""
    today = now().date()
    
    # Obtener datos agregados
    data = QualityTest.objects.filter(checked_at__date=today).aggregate(
        total=Count('id'),
        passed=Count('id', filter=models.Q(result="Aprobado")),
        failed=Count('id', filter=models.Q(result="Rechazado"))
    )

    # Guardar métricas en historial
    QualityMetricHistory.objects.update_or_create(
        date=today,
        defaults={
            'total_tests': data['total'],
            'passed_tests': data['passed'],
            'failed_tests': data['failed']
        }
    )

    return Response({"message": "Métricas generadas correctamente"})

@api_view(['GET'])
def quality_trend(request):
    """Devuelve la cantidad de pruebas aprobadas y rechazadas por día."""
    data = QualityMetricHistory.objects.order_by("date")

    response_data = {
        "labels": [entry.date.strftime("%Y-%m-%d") for entry in data],
        "approved": [entry.passed_tests for entry in data],
        "rejected": [entry.failed_tests for entry in data]
    }

    return Response(response_data)

@api_view(['GET'])
def failure_distribution(request):
    """Devuelve la cantidad de fallos por producto y tipo de fallo."""
    data = (
        QualityTest.objects.filter(result="Rechazado")
        .values("product__name", "parameter")
        .annotate(failures=Count("id"))
    )

    products = {}
    for entry in data:
        product_name = entry["product__name"]
        if product_name not in products:
            products[product_name] = {}
        products[product_name][entry["parameter"]] = entry["failures"]

    return Response(products)

@api_view(['GET'])
def best_worst_products(request):
    """Devuelve los 5 productos con mejor y peor calidad."""
    best = (
        QualityMetricHistory.objects.order_by("-passed_tests")[:5]
        .values("date", "passed_tests")
    )
    worst = (
        QualityMetricHistory.objects.order_by("-failed_tests")[:5]
        .values("date", "failed_tests")
    )

    return Response({
        "best_products": list(best),
        "worst_products": list(worst)
    })



