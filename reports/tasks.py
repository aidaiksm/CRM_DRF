from io import BytesIO
from celery import task
import weasyprint
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.conf import settings
from .models import Report

@task
def report_created(report_id):
    report = Report.objects.get(id=report_id)
    subject = f'Your report under id no. {report.id}'
    message = f'Hey, {report.author}!\n' \
              f'Your report has been submitted and is currently under review.' \
              f'Thank you for your contribution!'

    mail_sent = send_mail(subject, message, 'kasymaidai@gmail.com', [report.author.email])

    #generate PDF
    html = render_to_string('pdf.html', {'report': report})
    out = BytesIO()
    weasyprint.HTML(string=html).write_pdf(out)

    #attach PDF
    mail_sent.attach(f'report_{report.id}.pdf', out.getvalue(), 'application/pdf')

    mail_sent.send()
    return mail_sent


