import re
from presidio_analyzer import AnalyzerEngine

analyzer = AnalyzerEngine()

class PIIExtractor:
    def __init__(self):
        self.aadhaar_regex = r"\b\d{4}\s?\d{4}\s?\d{4}\b" 
        self.pan_regex = r"\b[A-Z]{5}\d{4}[A-Z]\b"
        self.ATM_CARD_PATTERN = r'\b\d{4}\s?\d{4}\s?\d{4}\s?\d{4}\b'
        self.DRIVING_LICENSE_PATTERN = r'\b[A-Z]{2}\d{2}\s?\d{4}\s?\d{4}\b'
        self.PASSPORT_PATTERN = r'\b[A-Z]{1}\d{7}\b'
        self.voter_id_regex = r"\b[A-Z]{3}\s?\d{7}\b"

    
    def getAllSensitiveData(self, text):
        aadhaarNums = re.findall(self.aadhaar_regex,  text)
        PANs = re.findall(self.pan_regex, text)
        DLs = re.findall(self.DRIVING_LICENSE_PATTERN, text)
        voterIDs = re.findall(self.voter_id_regex, text)
        ATMs = re.findall(self.ATM_CARD_PATTERN, text)
        passports = re.findall(self.PASSPORT_PATTERN, text)

        text = re.sub(self.aadhaar_regex, "[AADHAAR REDACTED]", text)
        text = re.sub(self.pan_regex,"[PAN REDACTED]", text)
        text = re.sub(self.DRIVING_LICENSE_PATTERN,"[DRIVING LICENCE REDACTED]", text)
        text = re.sub(self.voter_id_regex,"[EPIC REDACTED]", text)
        text = re.sub(self.ATM_CARD_PATTERN,"[ATM NUMBER REDACTED]", text)
        text = re.sub(self.PASSPORT_PATTERN,"[PASSPORT REDACTED]", text)

        returnObj = {
            "Aadhaar": aadhaarNums,
            "PAN": PANs,
            "DL": DLs,
            "Voter": voterIDs,
            "ATM": ATMs,
            "Passport": passports
        }

        results = analyzer.analyze(text=text, language="en")

        for i in results:
            if(i.entity_type not in returnObj):
                returnObj[i.entity_type] = []

            returnObj[i.entity_type].append(text[i.start: i.end])
            
        return returnObj
