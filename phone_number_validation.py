"Module to facilitate phone number validation"
from typing import Tuple
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException
from exceptions.Bad_Request import Bad_Request

def validate_phone_number(phone_number: str) -> Tuple:
    """Validates phone number. If invalid, raises error"""

    try:
        # Parse phone number
        phone_number = phonenumbers.parse(phone_number)
        
        # Return formated phone number if it's valid
        if phonenumbers.is_valid_number(phone_number):
            return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
    except NumberParseException as error:
        raise Bad_Request(error.args[0], "phone_number") from error

    raise Bad_Request("Phone number is invalid", "phone_number")
