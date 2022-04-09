import re
from django.core.exceptions import ValidationError

class CustomPasswordValidator:
    def validate(self, password):
        if re.match(
                r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$",
                password
            ) is None:
            raise ValidationError(
                "비밀번호가 유효성을 충족하지 못하였습니다.",
                code="invalid_password",
                params={'password': password},
                )
        return True

    def get_help_text(self):
        return "8글자 이상이며 특수문자, 숫자를 포함해야 합니다."
