from django.contrib import admin
from django.http import HttpResponse
from django.urls import reverse
from django.utils.safestring import mark_safe

from reports.models import Report, Status
import csv
import datetime

def export_to_csv(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    content_disposition = 'attachment; filename={opts.verbose_name}.csv'
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = content_disposition
    writer = csv.writer(response)

    fields = [field for field in opts.get_fields() if not\
              field.many_to_many and not field.one_to_many]
    writer.writerow([field.verbose_name for field in fields])
    for obj in queryset:
        data_row = []
        for field in fields:
            value = getattr(obj, field.name)
            if isinstance(value, datetime.datetime):
                value = value.strftime('%d/%m/%Y')
            data_row.append(value)
        writer.writerow(data_row)
    return response
export_to_csv.short_description = 'Export to CSV'


class StatusInline(admin.TabularInline):
    model = Status


def report_pdf(obj):
    url = reverse('reports:admin_report_pdf', args=[obj.id])
    return mark_safe(f'<a href="{url}"> PDF</a>')
report_pdf.short_description = 'PDF Copy'


class ReportAdmin(admin.ModelAdmin):
    model = Report
    actions = [export_to_csv]
    inlines = [StatusInline, ]
    list_display = ['id', 'author', report_pdf]




admin.site.register(Report, ReportAdmin)

