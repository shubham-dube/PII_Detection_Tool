import re
import pdfplumber
import os

class PIIExtractor:
    def __init__(self):
        self.aadhaar_regex = r"\b\d{4}\s?\d{4}\s?\d{4}\b"
        self.pan_regex = r"\b[A-Z]{5}\d{4}[A-Z]\b"
        self.dl_regex = r"\b[A-Z]{2}\d{2}\s?\d{7}\b"
        self.voter_id_regex = r"\b[A-Z]{3}\s?\d{7}\b"

    def extract_text_from_pdf(self, file_path):
        text = ''
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + '\n'
        return text

    def extract_text_from_file(self, file_path):
        with open(file_path, 'r') as file:
            text = file.read()
        return text

    def extract_text_from_string(self, input_string):
        return input_string

    def find_pii_in_text(self, text):
        aadhaar_matches = re.findall(self.aadhaar_regex, text)
        pan_matches = re.findall(self.pan_regex, text)
        dl_matches = re.findall(self.dl_regex, text)
        voter_id_matches = re.findall(self.voter_id_regex, text)

        return {
            'Aadhaar': aadhaar_matches,
            'PAN': pan_matches,
            'Driver’s License': dl_matches,
            'Voter ID': voter_id_matches
        }

if __name__ == "__main__":
    extractor = PIIExtractor()

    user_input = input("Enter the file path (PDF/TXT) or a string with PII data: ")

    if os.path.isfile(user_input):
        if user_input.lower().endswith('.pdf'):
            extracted_text = extractor.extract_text_from_pdf(user_input)
            pii_matches = extractor.find_pii_in_text(extracted_text)
            input_type = "PDF File"

        elif user_input.lower().endswith('.txt'):
            extracted_text = extractor.extract_text_from_file(user_input)
            pii_matches = extractor.find_pii_in_text(extracted_text)
            input_type = "Text File"
        else:
            print("Unsupported file format. Please provide a PDF or TXT file.")
            exit(1)
    else:
        extracted_text = extractor.extract_text_from_string(user_input)
        pii_matches = extractor.find_pii_in_text(extracted_text)
        input_type = "String"

    print(f"\nDetected PII from {input_type}:")
    for pii_type, matches in pii_matches.items():
        if matches:
            print(f"{pii_type}: {matches}")
        else:
            print(f"No {pii_type} found in {input_type}.")

