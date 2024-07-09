from abc import ABC, abstractmethod
from typing import List
import csv
import docx
import subprocess

class QuoteModel:
    """Quote Model that represents the qoute"""

    """Initialize quote object with body and author"""
    def __init__(self, body, author):
        self.body = body
        self.author = author


class IngestorInterface(ABC):
    """Base class for Ingestor"""

    """Method to determine a file can ingested or not"""
    @abstractmethod
    def can_ingest(cls, path: str):
        return bool

    """Method to parse the input file"""
    @abstractmethod
    def parse(cls, path: str):
        return List[QuoteModel]


class TextIngestor(IngestorInterface):
    """ Ingestor for text file"""

    """method to determine csv file can be ingested or not"""
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        # Check if the file extension is .txt
        return path.endswith('.txt')

    """Method to parse the text file"""
    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        quotes = list()
        with open(path, 'r') as file:
            # extract quoute and author in to quotemodel object
            for line in file:
                if len(line) > 0:
                    body, author = line.split(' - ')
                    quotes.append(QuoteModel(body, author))
        return quotes


class PdfIngestor(IngestorInterface):
    """Ingestor for PDF file"""

    """method to determine pdf file can be ingested or not"""
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        # Check if the file extension is .pdf
        return path.endswith('.pdf')

    """Method to parse the pdf file"""
    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        quotes = list()
        output = subprocess.run(['pdftotext', path, '-'], capture_output=True, text=True)
        extracted_text = output.stdout
        print(extracted_text)
        # extract quoute and author in to quotemodel object
        for line in extracted_text:
            if len(line) > 0:
                body, author = line.split(' - ')
                quotes.append(QuoteModel(body, author))
        return quotes


class CsvIngestor(IngestorInterface):
    """Ingestor for CSV file"""

    """method to determine csv file can be ingested or not"""
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        # Check if the file extension is .csv
        return path.endswith('.csv')

    """Method to parse the text file"""
    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        quotes = list()
        with open(path, 'r') as file:
            reader = csv.DictReader(file)
            # extract quoute and author in to quotemodel object
            for line in reader:
                body = line["body"]
                author = line["author"]
                quotes.append(QuoteModel(body, author))
        return quotes


class DocxIngestor(IngestorInterface):
    """Ingestor for doc file"""

    """method to determine docx file can be ingested or not"""
    @classmethod
    def can_ingest(cls, path: str) -> bool:
        # Check if the file extension is .docx
        return path.endswith('.docx')

    """Method to parse the text file"""
    @classmethod
    def parse(cls, path: str) -> List[QuoteModel]:
        quotes = list()
        doc = docx.Document(path)
        paragraphs_text = ""
        # read docx file content in variable
        for paragraph in doc.paragraphs:
            paragraphs_text += paragraph.text + "\n"
        # extract quoute and author in to quotemodel object
        for line in paragraphs_text:
            if len(line) > 0:
                body, author = line.split(' - ')
                quotes.append(QuoteModel(body, author))
        return quotes


class Ingestor(IngestorInterface):
    """A common interface for ingestor"""

    ingestors = [CsvIngestor, DocxIngestor, PdfIngestor, TextIngestor]

    """This function used to determine whether a file can be ingested or not"""
    def can_file_be_ingested(file_path: str) -> bool:
        ingestors = [CsvIngestor, DocxIngestor, PdfIngestor, TextIngestor]

        for ingestor in ingestors:
            if ingestor.can_ingest(file_path):
                return True
        return False

    """ Parse method for all file types"""
    @classmethod
    def parse(cls, path: str):
        for ingestor in cls.ingestors:
            if ingestor.can_ingest(path):
                return ingestor.parse(path)
        raise ValueError(f'No suitable ingestor found for file: {path}')

"""load qoutes from qoute files"""
def load_quotes(quote_files):
    quotes = []
    for file in quote_files:
        try:
            quotes.extend(Ingestor.parse(file))
        except Exception as e:
            print(f"Error loading file {file}: {e}")
    return quotes if quotes else None
