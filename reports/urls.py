from django.urls import path

from reports import views


app_name = 'reports'
urlpatterns = [
    path('<int:report_id>/pdf/', views.admin_report_pdf, name='admin_report_pdf'),
]