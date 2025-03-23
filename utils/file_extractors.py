# use pip install presidio-analyzer presidio-anonymizer to install the required packages
import fitz  
import docx
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# Initialize Presidio engines
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def extract_text_from_pdf(pdf_path):
    """Extracts text from a PDF file."""
    text = ""
    with fitz.open(pdf_path) as doc:
        for page in doc:
            text += page.get_text()
    return text

def extract_text_from_docx(docx_path):
    """Extracts text from a DOCX file."""
    doc = docx.Document(docx_path)
    return "\n".join([para.text for para in doc.paragraphs])

def redact_pii(text):
    """Redacts PII (phone numbers and email addresses) using Presidio."""
    # Analyze text for PII entities (phone numbers and emails)
    results = analyzer.analyze(text=text, entities=["PHONE_NUMBER", "EMAIL_ADDRESS"], language='en')
    
    # Anonymize detected PII entities
    redacted_text = anonymizer.anonymize(text, results).text
    
    return redacted_text

def get_file_text(file_path):
    """Extracts text from a file and redacts any PII."""
    if file_path.endswith(".pdf"):
        text = extract_text_from_pdf(file_path)
    elif file_path.endswith(".docx"):
        text = extract_text_from_docx(file_path)
    else:
        return ""  # If file is not PDF or DOCX, return empty string
    
    # Redact PII from the extracted text
    redacted_text = redact_pii(text)
    
    return redacted_text
