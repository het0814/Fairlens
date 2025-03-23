import fitz  # PyMuPDF for PDF extraction
import docx
from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# Initialize Presidio engines
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def extract_text(file_path):
    """Extracts text from PDF or DOCX files."""
    text = ""

    # Handle PDF files
    if file_path.endswith(".pdf"):
        with fitz.open(file_path) as doc:
            for page in doc:
                text += page.get_text()

    # Handle DOCX files
    elif file_path.endswith(".docx"):
        doc = docx.Document(file_path)
        text = "\n".join([para.text for para in doc.paragraphs])

    else:
        print(f"Unsupported file format: {file_path}")
    
    return text

def redact_pii(text):
    """Redacts PII using Presidio."""
    # Analyze text for PII entities
    results = analyzer.analyze(text=text, entities=[
        "PHONE_NUMBER", "EMAIL_ADDRESS",
    ], language='en')

    # Anonymize detected PII (no need for explicit config)
    redacted_text = anonymizer.anonymize(text, results).text

    return redacted_text

def process_file(file_path):
    """Processes a PDF or DOCX file, extracts text, and redacts PII."""
    # Extract text from the file
    text = extract_text(file_path)
    
    if not text.strip():
        return "No valid content extracted."

    # Redact PII
    redacted_text = redact_pii(text)
    
    return redacted_text
