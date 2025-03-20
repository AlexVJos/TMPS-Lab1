from abc import ABC, abstractmethod
from .models import Contract, Report, Note, Attachment


# --------------------------------
# 1. Factory Method Pattern
# --------------------------------
class DocumentCreator(ABC):
    @abstractmethod
    def create_document(self, **kwargs):
        pass

    def register_document(self, **kwargs):
        document = self.create_document(**kwargs)
        document.save()
        return document


class ContractCreator(DocumentCreator):
    def create_document(self, **kwargs):
        return Contract(**kwargs)


class ReportCreator(DocumentCreator):
    def create_document(self, **kwargs):
        return Report(**kwargs)


class NoteCreator(DocumentCreator):
    def create_document(self, **kwargs):
        return Note(**kwargs)


# --------------------------------
# 2. Abstract Factory Pattern
# --------------------------------
class DocumentPackageFactory(ABC):
    @abstractmethod
    def create_document(self, **kwargs):
        pass

    @abstractmethod
    def create_attachment(self, document, **kwargs):
        pass


class ContractPackageFactory(DocumentPackageFactory):
    def create_document(self, **kwargs):
        contract = Contract(**kwargs)
        contract.save()
        return contract

    def create_attachment(self, document, **kwargs):
        attachment = Attachment(contract=document, **kwargs)
        attachment.save()
        return attachment


class ReportPackageFactory(DocumentPackageFactory):
    def create_document(self, **kwargs):
        report = Report(**kwargs)
        report.save()
        return report

    def create_attachment(self, document, **kwargs):
        attachment = Attachment(report=document, **kwargs)
        attachment.save()
        return attachment


class NotePackageFactory(DocumentPackageFactory):
    def create_document(self, **kwargs):
        note = Note(**kwargs)
        note.save()
        return note

    def create_attachment(self, document, **kwargs):
        attachment = Attachment(note=document, **kwargs)
        attachment.save()
        return attachment