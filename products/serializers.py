from rest_framework import serializers
from .models import Product, ProductHistory

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at']  # Evita que sean modificados manualmente

class ProductHistorySerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    admin_full_name = serializers.SerializerMethodField()

    class Meta:
        model = ProductHistory
        fields = '__all__'

    def get_admin_full_name(self, obj):
        if obj.admin:
            return f"{obj.admin.first_name} {obj.admin.last_name}"
        return "Desconocido"