import re

phone_regex = re.compile(r'^\+998(20|33|71|77|90|91|93|94|95|97|98|99)\d{7}$')

async def check_phone_number(phone_number):
    if re.fullmatch(phone_regex, phone_number):
        return True
    return False