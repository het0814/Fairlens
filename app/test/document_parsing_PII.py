from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine

# Initialize Presidio Analyzer and Anonymizer
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

def redact_pii(text):
    # Analyze text for PII (Phone numbers and Emails)
    results = analyzer.analyze(text=text, entities=["PHONE_NUMBER", "EMAIL_ADDRESS"], language='en')
    
    # Anonymize detected PII
    redacted_text = anonymizer.anonymize(text=text, analyzer_results=results).text
    return redacted_text

# Example text to test
sample_text = """
Hello, my name is Parth. You can contact me at parth.patel@gmail.com or call me at 1234567890.
"""

# Run redaction
redacted = redact_pii(sample_text)

# Output results
print("Original Text:\n", sample_text)
print("\nRedacted Text:\n", redacted)
