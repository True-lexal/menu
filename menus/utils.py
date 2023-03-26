from django.core.validators import RegexValidator
from django.db import models


class MyUrlField(models.CharField):
    """
    Field validator
    """
    my_url_re = r'^[-a-zA-Z0-9_:/.]+\Z'
    validate_url = RegexValidator(
        my_url_re,
        'Допустимы цифры, латинские буквы и знаки  - _ : / .',
        'invalid',
    )
    default_validators = [validate_url]


class UrlSet:
    def __init__(self):
        self.url_set = set()


# Available set of urls in drawn menus
url_set = UrlSet()
