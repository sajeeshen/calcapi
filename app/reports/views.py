from datetime import datetime
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from reports import serializers
from rest_framework.authentication import TokenAuthentication
from django.db.models import Count
from django.db.models.functions import TruncMonth
from core.models import Report
from reports.utility import get_current_month
from reports.utility import get_current_year
from django.http import HttpResponse
import csv


class ReportManageView(generics.GenericAPIView):
        """
            Generate Report.
        """

        authentication_classes = (TokenAuthentication,)
        permission_classes = (IsAuthenticated,)
        serializer_class = serializers.ReportManageSerializer
        queryset = Report.objects.all()

        def get_queryset(self, month, year, report_type):
            """
            Based on the permission and the report type
            filter the result and return
            :param month: int
            :param year: int
            :param report_type: srting
            :return: object
            """
            query_result = None
            if report_type == "daily":
                if self.request.user.is_superuser:
                    query_result = (
                        Report.objects.values('user__email')
                            .annotate(total_hits=Count('name'),
                                      month=TruncMonth('created_at'))
                            .filter(created_at__date=datetime.now().date())
                                    )
                else:
                    query_result = (
                        Report.objects.values('user__email')
                            .annotate(total_hits=Count('name'),
                                      month=TruncMonth('created_at'))
                            .filter(created_at__date=datetime.now().date(),
                                    user=self.request.user)
                    )
            elif report_type == "monthly":
                if self.request.user.is_superuser:
                    query_result = (Report.objects.values('user__email')
                                    .annotate(total_hits=Count('name'),
                                              month=TruncMonth('created_at'))
                                    .filter(created_at__month=int(month),
                                            created_at__year=int(year))
                                    )
                else:
                    query_result = (Report.objects.values('user__email')
                                    .annotate(total_hits=Count('name'),
                                              month=TruncMonth('created_at'))
                                    .filter(created_at__month=int(month),
                                            created_at__year=int(year),
                                            user=self.request.user)
                                    )
            elif report_type == "yearly":
                if self.request.user.is_superuser:
                    query_result = (
                        Report.objects.values('user__email')
                            .annotate(total_hits=Count('name'),
                                      month=TruncMonth('created_at')).filter(
                            created_at__year=int(year))
                    )
                else:
                    query_result = (
                        Report.objects.values('user__email')
                            .annotate(total_hits=Count('name'),
                                      month=TruncMonth('created_at'))
                            .filter(
                            created_at__year=int(year),
                            user=self.request.user)
                    )
            return query_result

        def get(self, request, report_type, month=None, year=None):
            if month is None:
                month = get_current_month()
            if year is None:
                year = get_current_year()

            self.report_type = report_type
            rows = self.get_queryset(month, year, report_type)
            serializer = serializers.ReportManageSerializer(rows, many=True)
            response = HttpResponse(content_type='text/csv')
            response['Content-Disposition'] = \
                'attachment; filename="export.csv"'
            header = serializers.ReportManageSerializer.Meta.fields

            writer = csv.DictWriter(response, fieldnames=header)
            writer.writeheader()
            for row in serializer.data:
                writer.writerow(row)

            return response
