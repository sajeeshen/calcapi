from rest_framework import serializers
from core.models import Report


class CalculatorSerializer(serializers.Serializer):
    x = serializers.IntegerField(required=True)
    y = serializers.IntegerField(required=True)

    class Meta:
        model = Report
        exclude = ('id',)

    def create(self, validated_data):
        """ Extract the custom data and Save it into the Report"""
        user = validated_data.pop('user')
        action_name = validated_data.get('action_name')
        action_parameter = validated_data.get('action_parameter')
        return Report.objects.create(user=user,
                                     request_query=action_parameter,

                                     name=action_name)

    def validate(self, data):

        try:
            self.first_num = int(data.get('x'))
            self.second_num = int(data.get('y'))
        except Exception as err:
            raise serializers.ValidationError("Cant process, "
                                              "please check the input")
        return data
