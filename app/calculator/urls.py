from django.urls import path

from calculator import views

add = views.Calculator.as_view()
app_name = 'calculator'
urlpatterns = [
    path('add/', views.Calculator.as_view(),
         {'operation': 'add', 'admin_required': False}, name='add'),
    path('subtract/', views.Calculator.as_view(),
         {'operation': 'subtract', 'admin_required': False}, name='sub'),
    path('multiply/', views.Calculator.as_view(),
         {'operation': 'multiple', 'admin_required': False}, name='multiple'),
    path('divide/', views.Calculator.as_view(),
         {'operation': 'divide', 'admin_required': False}, name='divide'),
    path('power/', views.Calculator.as_view(),
         {'operation': 'power', 'admin_required': True}, name='power'),
    path('sqrt/', views.Calculator.as_view(),
         {'operation': 'sqrt', 'admin_required': True}, name='sqrt'),

]
