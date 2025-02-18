from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework import status
from .models import Product, ProductHistory
from .serializers import ProductSerializer, ProductHistorySerializer
from .permissions import IsAdminUser, IsOperatorOrAdmin

class ProductListView(generics.ListAPIView):
    """Lista de productos, accesible para admins y operadores."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOperatorOrAdmin]


class ProductDetailView(generics.RetrieveAPIView):
    """Detalle de un producto, accesible para admins y operadores."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOperatorOrAdmin]


class ProductCreateView(generics.CreateAPIView):
    """Creación de productos (solo admins)."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        product = serializer.save()
        # Guardar historial de creación
        ProductHistory.objects.create(
            product=product,
            admin=self.request.user,
            change_type="Creación"
        )


class ProductUpdateView(generics.UpdateAPIView):
    """Edición de productos (solo admins)."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def perform_update(self, serializer):
        product = serializer.save()
        # Guardar historial de modificación
        ProductHistory.objects.create(
            product=product,
            admin=self.request.user,
            change_type="Modificación"
        )


class ProductDeleteView(generics.DestroyAPIView):
    """Eliminación de productos (solo admins)."""
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminUser]

    def perform_destroy(self, instance):
        # Guardar historial antes de eliminar
        ProductHistory.objects.create(
            product=instance,
            admin=self.request.user,
            change_type="Eliminación"
        )
        instance.delete()


class ProductHistoryListView(generics.ListAPIView):
    """Lista de historial de productos (solo admins)."""
    queryset = ProductHistory.objects.all().order_by('-changed_at')
    serializer_class = ProductHistorySerializer
    permission_classes = [IsAdminUser]