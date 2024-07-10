from abc import ABC, abstractmethod
from typing import List
import csv
import docx
import subprocess
import os

class QuoteModel:
    """Quote Model that represents the qoute"""

    """Initialize quote object with body and author"""
    def __init__(self, body, author):
        self.body = body
        self.author = author

    """Override __str__ for dubugging"""
    def __str__(self):
        return f'Quote body: {self.body}, quote author: {self.author}"'

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
        # Ensure the tmp directory exists
        tmp_dir = './tmp'
        os.makedirs(tmp_dir, exist_ok=True)

        tmp = f'{tmp_dir}/{os.path.basename(path)}.txt'
        try:
            # Convert PDF to text using pdftotext
            subprocess.run(['pdftotext', path, tmp], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error converting PDF to text: {e}")
            return []

        quotes = []
        try:
            with open(tmp, 'r') as file:
                for line in file.readlines():
                    line = line.strip('\n\r').strip()
                    if len(line) > 0:
                        try:
                            body, author = line.split(' - ')
                            new_quote = QuoteModel(body, author)
                            quotes.append(new_quote)
                        except ValueError:
                            print(f"Error loading file {path}: not enough values to unpack (expected 2, got 1)")
        except FileNotFoundError as e:
            print(f"Error loading file {path}: {e}")
        finally:
            # Clean up the temporary file
            if os.path.exists(tmp):
                os.remove(tmp)

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
        quotes = []
        doc = docx.Document(path)

        for para in doc.paragraphs:
            if para.text != "":
                try:
                    body, author = para.text.split(' - ')
                    new_quote = QuoteModel(body, author)
                    quotes.append(new_quote)
                except ValueError:
                    print(f"Error loading file {path}: not enough values to unpack (expected 2, got 1)")

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
