from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.http import HttpResponse
from django.shortcuts import get_object_or_404

from documents.models import Contract, Report, Note
from .services import JSONExportBuilder, CSVExportBuilder, PDFExportBuilder, ExportDirector


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def export_document(request):
    document_type = request.GET.get('document_type')
    document_id = request.GET.get('document_id')
    export_format = request.GET.get('format', 'json')

    document = None
    if document_type == 'contract':
        document = get_object_or_404(Contract, id=document_id)
    elif document_type == 'report':
        document = get_object_or_404(Report, id=document_id)
    elif document_type == 'note':
        document = get_object_or_404(Note, id=document_id)
    else:
        return Response({'error': 'Invalid document type'}, status=400)

    if document.author != request.user:
        return Response({'error': 'Access denied'}, status=403)

    builder = None
    content_type = ''
    file_extension = ''

    if export_format == 'json':
        builder = JSONExportBuilder()
        content_type = 'application/json'
        file_extension = 'json'
    elif export_format == 'csv':
        builder = CSVExportBuilder()
        content_type = 'text/csv'
        file_extension = 'csv'
    elif export_format == 'pdf':
        builder = PDFExportBuilder()
        content_type = 'application/pdf'
        file_extension = 'pdf'
    else:
        return Response({'error': 'Invalid export format'}, status=400)

    director = ExportDirector(builder)
    result = director.build_export(document)

    response = HttpResponse(result, content_type=content_type)
    response['Content-Disposition'] = f'attachment; filename="{document.title}.{file_extension}"'

    return response