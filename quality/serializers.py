from rest_framework import serializers
from .models import QualityTest, QualityRule, QualityCheck, QualityHistory

class QualityRuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityRule
        fields = '__all__'


class QualityTestSerializer(serializers.ModelSerializer):
    rules = QualityRuleSerializer(many=True, read_only=True)

    class Meta:
        model = QualityTest
        fields = '__all__'


class QualityCheckSerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityCheck
        fields = '__all__'
        read_only_fields = ['checked_by', 'checked_at']


class QualityHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = QualityHistory
        fields = '__all__'
