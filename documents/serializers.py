from rest_framework import serializers
from .models import DocumentType, Contract, Report, Note, Attachment


class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentType
        fields = '__all__'


class AttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attachment
        fields = ['id', 'file', 'description', 'uploaded_at']


class ContractSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Contract
        fields = ['id', 'title', 'document_type', 'unique_id', 'author', 'status',
                  'version', 'created_at', 'updated_at', 'party_name', 'start_date',
                  'end_date', 'contract_value', 'terms_conditions', 'attachments']
        read_only_fields = ['id', 'unique_id', 'created_at', 'updated_at']


class ReportSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Report
        fields = ['id', 'title', 'document_type', 'unique_id', 'author', 'status',
                  'version', 'created_at', 'updated_at', 'report_date', 'department',
                  'summary', 'data', 'attachments']
        read_only_fields = ['id', 'unique_id', 'created_at', 'updated_at']


class NoteSerializer(serializers.ModelSerializer):
    attachments = AttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Note
        fields = ['id', 'title', 'document_type', 'unique_id', 'author', 'status',
                  'version', 'created_at', 'updated_at', 'content', 'priority', 'attachments']
        read_only_fields = ['id', 'unique_id', 'created_at', 'updated_at']