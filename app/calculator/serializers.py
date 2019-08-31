from rest_framework import serializers
from core.models import Report


class CalculatorSerializer(serializers.Serializer):
    x = serializers.IntegerField(required=True)
    y = serializers.IntegerField(required=True)

    class Meta:
        model = Report
        exclude = ('id',)

    def create(self, validated_data):
        user = validated_data.pop('user')
        action_name = validated_data.get('action_name')
        action_parameter = validated_data.get('action_parameter')
        return Report.objects.create(user=user,
                                     request_query=action_parameter,
                                     name=action_name)
