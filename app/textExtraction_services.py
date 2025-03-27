import fitz
import docx
from io import BytesIO
# from presidio_analyzer import AnalyzerEngine
# from presidio_anonymizer import AnonymizerEngine

# def redact_pii(text):
#     # Redacts PII (phone numbers and email addresses) using Presidio.
#     # Analyze text for PII entities (phone numbers and emails)
#     results = analyzer.analyze(text=text, entities=["PHONE_NUMBER", "EMAIL_ADDRESS"], language='en')
#     # Anonymize detected PII entities
#     redacted_text = anonymizer.anonymize(text, results).text
    
#     return redacted_text


def extract_text(file,file_name):
    file_bytes = BytesIO(file.read())  # Store the file in memory
    if file_name.endswith(".pdf"):
        text = ""
        with fitz.open(stream=file_bytes.getvalue(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
        return text
    elif file_name.endswith(".docx"):
        doc = docx.Document(file_bytes)
        text = "\n".join([para.text for para in doc.paragraphs])
        return text
