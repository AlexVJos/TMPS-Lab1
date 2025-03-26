from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import DocumentType, Contract, Report, Note
from .serializers import (
    DocumentTypeSerializer,
    ContractSerializer,
    ReportSerializer,
    NoteSerializer,
)
from .factories import (
    ContractCreator,
    ContractPackageFactory,
)
from .builders import ContractBuilder, ReportBuilder, DocumentDirector
from notifications.singleton import NotificationService


class DocumentTypeViewSet(viewsets.ModelViewSet):
    queryset = DocumentType.objects.all()
    serializer_class = DocumentTypeSerializer


class ContractViewSet(viewsets.ModelViewSet):
    queryset = Contract.objects.all()
    serializer_class = ContractSerializer

    @action(detail=True, methods=['post'])
    def clone(self, request, pk=None):
        original = self.get_object()
        custom_field = request.data.get('custom_notes')
        cloned = original.clone()
        if custom_field:
            cloned.custom_notes = custom_field
        cloned.save()

        notification_service = NotificationService()
        notification_service.notify('document_cloned', {
            'document': cloned,
            'original': original,
            'user': request.user
        })

        return Response(self.get_serializer(cloned).data)

    @action(detail=False, methods=['post'])
    def create_using_builder(self, request):
        try:
            author = request.user
            document_type = get_object_or_404(DocumentType, id=request.data.get('document_type'))

            # builder using
            builder = ContractBuilder()
            director = DocumentDirector(builder)

            if request.data.get('build_type') == 'minimal':
                contract = director.make_minimal_document(
                    title=request.data.get('title'),
                    author=author,
                    document_type=document_type
                )
            else:
                contract = director.make_standard_contract(
                    title=request.data.get('title'),
                    author=author,
                    document_type=document_type,
                    party_name=request.data.get('party_name'),
                    start_date=request.data.get('start_date'),
                    end_date=request.data.get('end_date'),
                    value=request.data.get('contract_value')
                )

            contract.save()

            notification_service = NotificationService()
            notification_service.notify('document_created', {
                'document': contract,
                'user': request.user
            })

            return Response(self.get_serializer(contract).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def create_using_factory(self, request):
        try:
            # factory method
            creator = ContractCreator()

            contract_data = {
                'title': request.data.get('title'),
                'author': request.user,
                'document_type_id': request.data.get('document_type'),
                'status': 'draft',
                'party_name': request.data.get('party_name'),
                'start_date': request.data.get('start_date'),
                'end_date': request.data.get('end_date'),
                'contract_value': request.data.get('contract_value'),
                'terms_conditions': request.data.get('terms_conditions', '')
            }

            contract = creator.register_document(**contract_data)

            return Response(self.get_serializer(contract).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=['post'])
    def create_with_attachments(self, request):
        try:
            with transaction.atomic():
                # abstract factory
                factory = ContractPackageFactory()

                contract_data = {
                    'title': request.data.get('title'),
                    'author': request.user,
                    'document_type_id': request.data.get('document_type'),
                    'status': 'draft',
                    'party_name': request.data.get('party_name'),
                    'start_date': request.data.get('start_date'),
                    'end_date': request.data.get('end_date'),
                    'contract_value': request.data.get('contract_value'),
                    'terms_conditions': request.data.get('terms_conditions', '')
                }

                contract = factory.create_document(**contract_data)

                # Создание вложений, если они есть в запросе
                attachments_data = request.data.get('attachments', [])
                for attachment_data in attachments_data:
                    factory.create_attachment(
                        document=contract,
                        file=attachment_data.get('file'),
                        description=attachment_data.get('description')
                    )

                return Response(self.get_serializer(contract).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

    @action(detail=True, methods=['post'])
    def clone(self, request, pk=None):
        # prototype using
        original = self.get_object()
        cloned = original.clone()
        cloned.save()
        return Response(self.get_serializer(cloned).data)

    @action(detail=False, methods=['post'])
    def create_using_builder(self, request):
        try:
            author = request.user
            document_type = get_object_or_404(DocumentType, id=request.data.get('document_type'))

            # builder using
            builder = ReportBuilder()
            director = DocumentDirector(builder)

            data_sections = request.data.get('data_sections', {})

            report = director.make_comprehensive_report(
                title=request.data.get('title'),
                author=author,
                document_type=document_type,
                date=request.data.get('report_date'),
                department=request.data.get('department'),
                summary=request.data.get('summary'),
                data_sections=data_sections
            )

            report.save()
            return Response(self.get_serializer(report).data, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    @action(detail=True, methods=['post'])
    def clone(self, request, pk=None):
        # prototype using
        original = self.get_object()
        cloned = original.clone()
        cloned.save()
        return Response(self.get_serializer(cloned).data)
