import re
from marshmallow import fields, ValidationError


class PasswordField(fields.String):
    def _validate(self, value):
        super()._validate(value)
        if not re.search(r'^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$%^&*-]).{8,}$', value):
            raise ValidationError(
                'Password must contain at least 8 characters with at least one lowercase letter, one uppercase letter, one digit, and one special character')
