import re
import phonenumbers
from phonenumbers import parse
from phonenumbers.phonenumberutil import NumberParseException
from phonenumbers import PhoneNumberFormat,format_number

def validate_number(cleaner, region="IN"):
    try:
        parsed = parse(cleaner, region)
        if not phonenumbers.is_possible_number(parsed):
              return False
        if not phonenumbers.is_valid_number(parsed):
              return False
        return True
    except NumberParseException:
        return False
        

def clean_number(phonenumber):
    cleaned = re.sub(r'[\s\-\()\.\,]','',phonenumber)
    if cleaned.count("+") > 1:
        cleaned = cleaned.replace("+", "")
    elif cleaned.startswith("+"):
        pass
    else:
        cleaned = cleaned.replace("+", "")
    if not cleaned.startswith('+'):
     cleaned = cleaned.lstrip('0')
     
    return cleaned

def parse_number(cleaned, region="IN"):
    try:
        parsed = parse(cleaned, region)
        return parsed 
    except NumberParseException:
        return None

def normaliser(parsed_number):
        if parsed_number is None:
            return None
        
        try:
            return{

            "E164": format_number(parsed_number, PhoneNumberFormat.E164),
            "INTERNATIONAL": format_number(parsed_number, PhoneNumberFormat.INTERNATIONAL),
            "NATIONAL": format_number(parsed_number, PhoneNumberFormat.NATIONAL)
            }
        
       
        except Exception :
            return None


def parse_pipeline(raw_input,region = "IN"):
    cleaner = clean_number(raw_input)
    if not validate_number(cleaner, region):
        return {
            "success": False,
            "error": "Invalid phone number",
            "parsed": None,
            "normalized": None
        }
    
    
    parsed = parse_number(cleaner, region)
    normalized = normaliser(parsed)
    return {
            "success": True,
            "error": None,
            "parsed": parsed,
            "normalized": normalized
        }












# number = input("Enter your number with country code: ")

# if not validate_number(number):
#     print("Phone number is invalid.", validate_number(number))
#     exit()
# else:
#     print("Phone number is valid.", validate_number(number))

# parsed_num = parse_number(number)
# print("Parsed Number:", parsed_num)

# if parsed_num:
#     formatted_number = normaliser(parsed_num)
#     print("Formatted Number:", formatted_number)




