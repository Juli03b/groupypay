from exceptions.BadRequest import BadRequest
from typing import Tuple
import phonenumbers
from phonenumbers.phonenumberutil import NumberParseException

def validate_phone_number(phone_number: str) -> Tuple:
    try:
        phone_number = phonenumbers.parse(phone_number)

        if phonenumbers.is_valid_number(phone_number):
            # If number is valid and parsable, format it and return it
            return phonenumbers.format_number(phone_number, phonenumbers.PhoneNumberFormat.E164)
        else:
            raise BadRequest("Phone number is invalid", "phone_number")
    except NumberParseException as e:
        error_msg = e.args[0]

        raise BadRequest(error_msg, "phone_number")
    