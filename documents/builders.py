from abc import ABC, abstractmethod
from .models import Contract, Report


class DocumentBuilder(ABC):
    @abstractmethod
    def set_title(self, title):
        pass

    @abstractmethod
    def set_author(self, author):
        pass

    @abstractmethod
    def set_document_type(self, document_type):
        pass

    @abstractmethod
    def get_result(self):
        pass


class ContractBuilder(DocumentBuilder):
    def __init__(self):
        self.contract = Contract()
        self.contract.terms_conditions = ""

    def set_title(self, title):
        self.contract.title = title
        return self

    def set_author(self, author):
        self.contract.author = author
        return self

    def set_document_type(self, document_type):
        self.contract.document_type = document_type
        return self

    def set_party_name(self, party_name):
        self.contract.party_name = party_name
        return self

    def set_date_range(self, start_date, end_date):
        self.contract.start_date = start_date
        self.contract.end_date = end_date
        return self

    def set_value(self, value):
        self.contract.contract_value = value
        return self

    def add_terms_section(self, section_title, section_content):
        section = f"\n## {section_title}\n\n{section_content}"
        self.contract.terms_conditions += section
        return self

    def get_result(self):
        return self.contract


class ReportBuilder(DocumentBuilder):
    def __init__(self):
        self.report = Report()
        self.report.data = {}

    def set_title(self, title):
        self.report.title = title
        return self

    def set_author(self, author):
        self.report.author = author
        return self

    def set_document_type(self, document_type):
        self.report.document_type = document_type
        return self

    def set_report_date(self, date):
        self.report.report_date = date
        return self

    def set_department(self, department):
        self.report.department = department
        return self

    def set_summary(self, summary):
        self.report.summary = summary
        return self

    def add_data_section(self, section_name, data):
        if 'sections' not in self.report.data:
            self.report.data['sections'] = []

        self.report.data['sections'].append({
            'name': section_name,
            'data': data
        })
        return self

    def get_result(self):
        return self.report


class DocumentDirector:
    def __init__(self, builder):
        self.builder = builder

    def change_builder(self, builder):
        self.builder = builder

    def make_minimal_document(self, title, author, document_type):
        return self.builder \
            .set_title(title) \
            .set_author(author) \
            .set_document_type(document_type) \
            .get_result()

    def make_standard_contract(self, title, author, document_type, party_name, start_date, end_date, value):
        contract_builder = self.builder
        if not isinstance(contract_builder, ContractBuilder):
            raise ValueError("Builder must be a ContractBuilder")

        return contract_builder \
            .set_title(title) \
            .set_author(author) \
            .set_document_type(document_type) \
            .set_party_name(party_name) \
            .set_date_range(start_date, end_date) \
            .set_value(value) \
            .add_terms_section("General Terms", "These are the general terms of the contract.") \
            .add_terms_section("Payment Terms", "Payment shall be made within 30 days.") \
            .get_result()

    def make_comprehensive_report(self, title, author, document_type, date, department, summary, data_sections):
        report_builder = self.builder
        if not isinstance(report_builder, ReportBuilder):
            raise ValueError("Builder must be a ReportBuilder")

        report_builder \
            .set_title(title) \
            .set_author(author) \
            .set_document_type(document_type) \
            .set_report_date(date) \
            .set_department(department) \
            .set_summary(summary)

        for section_name, data in data_sections.items():
            report_builder.add_data_section(section_name, data)

        return report_builder.get_result()