from django.db import models
from django.utils.timezone import now

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.CharField(max_length=100)  # Ej: "Sensor de temperatura"
    sku = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class QualityTest(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="tests")
    checked_at = models.DateTimeField(default=now)
    result = models.CharField(max_length=20, choices=[("Aprobado", "Aprobado"), ("Rechazado", "Rechazado")])
    parameter = models.CharField(max_length=100)  # Ej: "Temperatura", "Presión"
    value = models.FloatField()
    fixed_at = models.DateTimeField(null=True, blank=True)  # Si se corrigió

    def __str__(self):
        return f"{self.product.name} - {self.parameter}: {self.result}"

class QualityMetricHistory(models.Model):
    """Histórico de métricas procesadas para el dashboard."""
    date = models.DateField(default=now)
    total_tests = models.IntegerField(default=0)
    passed_tests = models.IntegerField(default=0)
    failed_tests = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.date} - {self.total_tests} pruebas"
