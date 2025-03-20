from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import uuid
import copy


class DocumentMetadata(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='authored_documents')
    status = models.CharField(max_length=20, choices=[
        ('draft', 'Draft'),
        ('review', 'Under Review'),
        ('approved', 'Approved'),
        ('published', 'Published'),
        ('archived', 'Archived'),
    ], default='draft')
    version = models.IntegerField(default=1)

    class Meta:
        abstract = True


class DocumentType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    template = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Document(DocumentMetadata):
    title = models.CharField(max_length=255)
    document_type = models.ForeignKey(DocumentType, on_delete=models.CASCADE)
    unique_id = models.UUIDField(default=uuid.uuid4, editable=False)

    # Метод прототипа - создание копии документа
    def clone(self):
        new_document = copy.deepcopy(self)
        new_document.pk = None
        new_document.unique_id = uuid.uuid4()
        new_document.title = f"Copy of {self.title}"
        new_document.status = 'draft'
        new_document.version = 1
        new_document.created_at = timezone.now()
        new_document.updated_at = timezone.now()
        return new_document

    def __str__(self):
        return self.title

    class Meta:
        abstract = True


class Contract(Document):
    party_name = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    contract_value = models.DecimalField(max_digits=12, decimal_places=2)
    terms_conditions = models.TextField()


class Report(Document):
    report_date = models.DateField()
    department = models.CharField(max_length=100)
    summary = models.TextField()
    data = models.JSONField(default=dict)


class Note(Document):
    content = models.TextField()
    priority = models.IntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=1)


class Attachment(models.Model):
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, null=True, blank=True, related_name='attachments')
    report = models.ForeignKey(Report, on_delete=models.CASCADE, null=True, blank=True, related_name='attachments')
    note = models.ForeignKey(Note, on_delete=models.CASCADE, null=True, blank=True, related_name='attachments')
    file = models.FileField(upload_to='attachments/')
    description = models.CharField(max_length=255)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description