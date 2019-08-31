from django.urls import path
from reports import views


app_name = 'reports'

urlpatterns = [
    path('daily/', views.ReportManageView.as_view(),
         {'report_type': 'daily'} ,name='daily'),
    path('monthly/<int:month>/<int:year>',
         views.ReportManageView.as_view(),
         {'report_type': 'monthly'}, name='monthly'),
    path('yearly/<int:year>', views.ReportManageView.as_view(),
         {'report_type': 'yearly'}, name='yearly'),

]
