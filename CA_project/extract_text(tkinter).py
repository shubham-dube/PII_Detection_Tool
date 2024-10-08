import re
import pdfplumber
import os
from tkinter import Tk
from tkinter.filedialog import askopenfilename

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

    # Initialize Tkinter window for file dialog
    Tk().withdraw()  # We don't need a full GUI, so keep the root window from appearing
    file_path = askopenfilename(title="Select a PDF or Text File", filetypes=[("PDF files", "*.pdf"), ("Text files", "*.txt")])

    if file_path:
        # Check if it's a PDF file
        if file_path.lower().endswith('.pdf'):
            extracted_text = extractor.extract_text_from_pdf(file_path)
            pii_matches = extractor.find_pii_in_text(extracted_text)
            input_type = "PDF File"
        # Check if it's a text file
        elif file_path.lower().endswith('.txt'):
            extracted_text = extractor.extract_text_from_file(file_path)
            pii_matches = extractor.find_pii_in_text(extracted_text)
            input_type = "Text File"
        else:
            print("Unsupported file format. Please provide a PDF or TXT file.")
            exit(1)

        # Output the detected PII
        print(f"\nDetected PII from {input_type}:")
        for pii_type, matches in pii_matches.items():
            if matches:
                print(f"{pii_type}: {matches}")
            else:
                print(f"No {pii_type} found in {input_type}.")
    else:
        print("No file selected.")