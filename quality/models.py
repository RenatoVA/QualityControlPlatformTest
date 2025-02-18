from django.db import models
from django.contrib.auth import get_user_model
from products.models import Product, Category
import uuid

User = get_user_model()

class QualityTest(models.Model):
    """
    Representa una prueba de calidad asociada a un producto específico.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="quality_tests")
    name = models.CharField(max_length=100)  # Ejemplo: "Medición de Exactitud", "Resistencia"
    description = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product.name} - {self.name}"


class QualityRule(models.Model):
    """
    Reglas de calidad dentro de una prueba. Define parámetros e intervalos permitidos.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test = models.ForeignKey(QualityTest, on_delete=models.CASCADE, related_name="quality_rules")
    parameter = models.CharField(max_length=50)  # Ejemplo: "Temperatura", "Humedad"
    min_value = models.FloatField()
    max_value = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.test.name} - {self.parameter} ({self.min_value} - {self.max_value})"


class QualityCheck(models.Model):
    """
    Evaluación de una prueba de calidad. Contiene los valores ingresados y el resultado.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    test = models.ForeignKey(QualityTest, on_delete=models.CASCADE, related_name="quality_checks")
    checked_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    checked_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.test.name} - {self.checked_by.username} ({self.checked_at})"


class QualityCheckResult(models.Model):
    """
    Registro individual de cada medición dentro de un QualityCheck.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    quality_check = models.ForeignKey(QualityCheck, on_delete=models.CASCADE, related_name="results")
    rule = models.ForeignKey(QualityRule, on_delete=models.CASCADE)
    measured_value = models.FloatField()
    result = models.CharField(max_length=20, choices=[("Aceptado", "Aceptado"), ("Rechazado", "Rechazado")])

    def save(self, *args, **kwargs):
        """Lógica para determinar si la medición cumple con la regla de calidad."""
        if self.rule.min_value <= self.measured_value <= self.rule.max_value:
            self.result = "Aceptado"
        else:
            self.result = "Rechazado"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.rule.parameter}: {self.measured_value} → {self.result}"


class QualityHistory(models.Model):
    """
    Historial de cambios en las reglas de calidad.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    rule = models.ForeignKey(QualityRule, on_delete=models.CASCADE, related_name="history")
    field_changed = models.CharField(max_length=50)  # "min_value", "max_value"
    old_value = models.FloatField()
    new_value = models.FloatField()
    changed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    changed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.rule.test.name} - {self.field_changed}: {self.old_value} → {self.new_value}"
