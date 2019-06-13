from rest_framework import serializers
from .models import PerformanceMetrics

class CustomSerializer(serializers.ModelSerializer):

    def retain_fields_in_validation(self):
        return ['id']

    def run_validation(self, data=None):

        retain_fields = self.retain_fields_in_validation()

        retain_values = {}

        for field in retain_fields:
            retain_values[field] = data.get(field, None) if isinstance(data, dict) else None

        value = super().run_validation(data)

        for key in retain_values:
            value[key] = retain_values[key]  # restore

        return value


class PerformanceMetricsSerializer(CustomSerializer):
    id = serializers.ReadOnlyField()
    # recorded_date = serializers.SerializerMethodField('recorded_date')

    class Meta:
        model = PerformanceMetrics
        fields = '__all__'
