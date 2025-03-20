from abc import ABC, abstractmethod
import json


class DocumentExportBuilder(ABC):
    @abstractmethod
    def set_document(self, document):
        pass

    @abstractmethod
    def add_metadata(self):
        pass

    @abstractmethod
    def add_content(self):
        pass

    @abstractmethod
    def add_attachments(self):
        pass

    @abstractmethod
    def get_result(self):
        pass


class JSONExportBuilder(DocumentExportBuilder):
    def __init__(self):
        self.result = {}

    def set_document(self, document):
        self.document = document
        self.result = {}
        return self

    def add_metadata(self):
        self.result['metadata'] = {
            'id': str(self.document.id),
            'title': self.document.title,
            'unique_id': str(self.document.unique_id),
            'created_at': self.document.created_at.isoformat(),
            'updated_at': self.document.updated_at.isoformat(),
            'author': self.document.author.username,
            'status': self.document.status,
            'version': self.document.version,
            'document_type': self.document.document_type.name,
        }
        return self

    def add_content(self):
        self.result['content'] = {}

        if hasattr(self.document, 'party_name'):  # Contract
            self.result['content']['party_name'] = self.document.party_name
            self.result['content']['start_date'] = self.document.start_date.isoformat()
            self.result['content']['end_date'] = self.document.end_date.isoformat()
            self.result['content']['contract_value'] = str(self.document.contract_value)
            self.result['content']['terms_conditions'] = self.document.terms_conditions
        elif hasattr(self.document, 'report_date'):  # Report
            self.result['content']['report_date'] = self.document.report_date.isoformat()
            self.result['content']['department'] = self.document.department
            self.result['content']['summary'] = self.document.summary
            self.result['content']['data'] = self.document.data
        elif hasattr(self.document, 'content'):  # Note
            self.result['content']['content'] = self.document.content
            self.result['content']['priority'] = self.document.priority

        return self

    def add_attachments(self):
        self.result['attachments'] = []

        attachments = []
        if hasattr(self.document, 'attachments'):
            attachments = self.document.attachments.all()

        for attachment in attachments:
            self.result['attachments'].append({
                'id': attachment.id,
                'file': attachment.file.url if attachment.file else None,
                'description': attachment.description,
                'uploaded_at': attachment.uploaded_at.isoformat()
            })

        return self

    def get_result(self):
        return json.dumps(self.result, indent=4)


class CSVExportBuilder(DocumentExportBuilder):
    def __init__(self):
        self.rows = []
        self.headers = []

    def set_document(self, document):
        self.document = document
        self.rows = []
        self.headers = []
        return self

    def add_metadata(self):
        self.headers.extend(['ID', 'Title', 'Unique ID', 'Created At', 'Updated At',
                             'Author', 'Status', 'Version', 'Document Type'])

        metadata_row = [
            str(self.document.id),
            self.document.title,
            str(self.document.unique_id),
            self.document.created_at.isoformat(),
            self.document.updated_at.isoformat(),
            self.document.author.username,
            self.document.status,
            str(self.document.version),
            self.document.document_type.name
        ]

        self.rows.append(metadata_row)
        return self

    def add_content(self):
        if hasattr(self.document, 'party_name'):  # Contract
            self.headers.extend(['Party Name', 'Start Date', 'End Date', 'Value', 'Terms'])
            self.rows[0].extend([
                self.document.party_name,
                self.document.start_date.isoformat(),
                self.document.end_date.isoformat(),
                str(self.document.contract_value),
                self.document.terms_conditions[:100] + '...' if len(
                    self.document.terms_conditions) > 100 else self.document.terms_conditions
            ])
        elif hasattr(self.document, 'report_date'):  # Report
            self.headers.extend(['Report Date', 'Department', 'Summary'])
            self.rows[0].extend([
                self.document.report_date.isoformat(),
                self.document.department,
                self.document.summary[:100] + '...' if len(self.document.summary) > 100 else self.document.summary
            ])
        elif hasattr(self.document, 'content'):  # Note
            self.headers.extend(['Content', 'Priority'])
            self.rows[0].extend([
                self.document.content[:100] + '...' if len(self.document.content) > 100 else self.document.content,
                str(self.document.priority)
            ])

        return self

    def add_attachments(self):
        attachments = []
        if hasattr(self.document, 'attachments'):
            attachments = self.document.attachments.all()

        self.headers.append('Attachment Count')
        self.rows[0].append(str(attachments.count()))
        return self

    def get_result(self):
        output = [','.join(self.headers)]
        for row in self.rows:
            output.append(','.join([f'"{cell}"' if ',' in cell else cell for cell in row]))
        return '\n'.join(output)


class PDFExportBuilder(DocumentExportBuilder):
    def __init__(self):
        self.content = []

    def set_document(self, document):
        self.document = document
        self.content = ["PDF EXPORT SIMULATION"]
        return self

    def add_metadata(self):
        self.content.append("=== METADATA ===")
        self.content.append(f"ID: {self.document.id}")
        self.content.append(f"Title: {self.document.title}")
        self.content.append(f"Unique ID: {self.document.unique_id}")
        self.content.append(f"Created: {self.document.created_at.isoformat()}")
        self.content.append(f"Updated: {self.document.updated_at.isoformat()}")
        self.content.append(f"Author: {self.document.author.username}")
        self.content.append(f"Status: {self.document.status}")
        self.content.append(f"Version: {self.document.version}")
        self.content.append(f"Document Type: {self.document.document_type.name}")
        return self

    def add_content(self):
        self.content.append("\n=== CONTENT ===")

        if hasattr(self.document, 'party_name'):  # Contract
            self.content.append(f"Party Name: {self.document.party_name}")
            self.content.append(f"Start Date: {self.document.start_date.isoformat()}")
            self.content.append(f"End Date: {self.document.end_date.isoformat()}")
            self.content.append(f"Contract Value: {self.document.contract_value}")
            self.content.append("\nTerms and Conditions:")
            self.content.append(self.document.terms_conditions)
        elif hasattr(self.document, 'report_date'):  # Report
            self.content.append(f"Report Date: {self.document.report_date.isoformat()}")
            self.content.append(f"Department: {self.document.department}")
            self.content.append(f"Summary: {self.document.summary}")
            self.content.append("\nData:")
            self.content.append(json.dumps(self.document.data, indent=2))
        elif hasattr(self.document, 'content'):  # Note
            self.content.append(f"Content: {self.document.content}")
            self.content.append(f"Priority: {self.document.priority}")

        return self

    def add_attachments(self):
        self.content.append("\n=== ATTACHMENTS ===")

        # Определение связанных вложений в зависимости от типа документа
        attachments = []
        if hasattr(self.document, 'attachments'):
            attachments = self.document.attachments.all()

        if not attachments:
            self.content.append("No attachments found.")
        else:
            for attachment in attachments:
                self.content.append(f"- {attachment.description} ({attachment.file.name})")

        return self

    def get_result(self):
        return "\n".join(self.content)


class ExportDirector:
    def __init__(self, builder):
        self.builder = builder

    def change_builder(self, builder):
        self.builder = builder

    def build_export(self, document):
        return self.builder \
            .set_document(document) \
            .add_metadata() \
            .add_content() \
            .add_attachments() \
            .get_result()