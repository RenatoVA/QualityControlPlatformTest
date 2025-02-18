from rest_framework import serializers
from .models import Product, QualityTest, QualityMetricHistory

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'

class QualityTestSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityTest
        fields = '__all__'

class QualityMetricHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityMetricHistory
        fields = '__all__'