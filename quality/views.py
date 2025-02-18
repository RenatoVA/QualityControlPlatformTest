from rest_framework import viewsets, generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .models import QualityTest, QualityRule, QualityCheck, QualityHistory
from .serializers import (
    QualityTestSerializer, QualityRuleSerializer, QualityCheckSerializer, QualityHistorySerializer
)
from .permissions import IsAdminUser, IsOperatorOrAdmin


class QualityTestViewSet(viewsets.ModelViewSet):
    """
    CRUD para Pruebas de Calidad, solo administradores pueden modificar.
    """
    queryset = QualityTest.objects.all()
    serializer_class = QualityTestSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsOperatorOrAdmin]
        return [permission() for permission in permission_classes]


class QualityRuleViewSet(viewsets.ModelViewSet):
    """
    CRUD para Reglas de Calidad dentro de una prueba de calidad.
    """
    queryset = QualityRule.objects.all()
    serializer_class = QualityRuleSerializer

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            permission_classes = [IsAdminUser]
        else:
            permission_classes = [IsOperatorOrAdmin]
        return [permission() for permission in permission_classes]


class QualityCheckCreateView(generics.CreateAPIView):
    """
    Vista para registrar un nuevo chequeo de calidad.
    """
    queryset = QualityCheck.objects.all()
    serializer_class = QualityCheckSerializer
    permission_classes = [IsOperatorOrAdmin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Obtener la prueba de calidad asociada
        quality_test = get_object_or_404(QualityTest, id=request.data.get("quality_test"))
        
        # Evaluar los valores ingresados con las reglas de calidad
        results = []
        for rule in quality_test.rules.all():
            value = request.data.get(rule.parameter, None)
            if value is None:
                continue  # Si falta un valor, no evaluamos esa regla
            
            result = "Aceptado" if rule.min_value <= value <= rule.max_value else "Rechazado"
            results.append({
                "rule": rule.parameter,
                "value": value,
                "result": result
            })

        # Guardar el chequeo
        quality_check = serializer.save(checked_by=request.user)

        return Response({
            "quality_check": QualityCheckSerializer(quality_check).data,
            "results": results
        }, status=status.HTTP_201_CREATED)


class QualityHistoryListView(generics.ListAPIView):
    """
    Vista para consultar el historial de cambios en las reglas de calidad.
    """
    queryset = QualityHistory.objects.all().order_by('-changed_at')
    serializer_class = QualityHistorySerializer
    permission_classes = [IsAdminUser]
