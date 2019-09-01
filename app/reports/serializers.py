from rest_framework import serializers
from core.models import Report


class ReportManageSerializer(serializers.ModelSerializer):
    """ Serializer for Reports"""
    user_email = serializers.CharField(read_only=True, source="user__email")
    month = serializers.DateTimeField(read_only=True, format="%Y-%m")
    total_hits = serializers.IntegerField()


    class Meta:

        model = Report
        fields = ("total_hits", "user_email", "month")
