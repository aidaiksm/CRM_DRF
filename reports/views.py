from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from django.http import HttpResponse
from django.template.loader import render_to_string
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework import viewsets, filters, generics, mixins, status
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, IsAuthenticated
import weasyprint
from .serializers import *
from .permissions import IsReportAuthor
from .tasks import report_created


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['evaluation', 'flight_num']
    search_fields = ['body', 'suggestions']


    def get_serializer_context(self):
        return {'request': self.request}

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            permissions = [IsReportAuthor,]
        if self.action in ['retrieve', 'list']:
            permissions = [IsAdminUser, ]
        else:
            permissions = [IsAuthenticated, ]
        return [permission() for permission in permissions]


    @action(detail=False, methods=['get'])
    def submitted(self, request, pk=None):
        queryset = Report.objects.all()
        queryset = queryset.filter(author=request.user)
        serializer = ReportSerializer(queryset, many=True, context={'request':request})
        return Response(serializer.data)



class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAdminUser, IsReportAuthor]
    queryset = Comment.objects.all()

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            permissions = []
        else:
            permissions = [IsAdminUser]
        return [permission() for permission in permissions]


class StatusReportView(generics.CreateAPIView, mixins.DestroyModelMixin):
    serializer_class = StatusSerializer
    permission_classes = [IsAdminUser]

    def get_queryset(self):
        user = self.request.user
        report = Report.objects.get(pk=self.kwargs['pk'])
        return Status.objects.filter(user=user, report=report)

    def perform_create(self, serializer):
        if self.get_queryset().exists():
            raise ValidationError('The report is being processed')
        serializer.save(user=self.request.user, report=Report.objects.get(pk=self.kwargs['pk']))

    def delete(self, request, *args, **kwargs):
        if self.get_queryset().exists():
            self.get_queryset().delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            raise ValidationError('The report has not yet been processed')


@staff_member_required
def admin_report_pdf(request, report_id):
    report = get_object_or_404(Report, id=report_id)
    html = render_to_string('pdf.html',
                            {'report': report})

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename=report_{report.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response)
    return response
