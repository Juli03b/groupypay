from typing import Tuple
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

def validate_phone_number(phone_number: str) -> Tuple:
    error_msg = "Phone number is invalid, none saved"
    
    try:
        phone_number = phonenumbers.parse(phone_number)

        if phonenumbers.is_valid_number(phone_number):
            # If number is valid and parsable, format it and return it
            return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164), None
        else:
            print(phone_number)
    except NumberParseException as e:
        error_msg = e.args[0]
    
    return None, error_msg
    