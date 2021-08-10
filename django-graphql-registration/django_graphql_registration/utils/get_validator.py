from django_graphql_registration.utils import (get_setting_or_throw,
                                               import_class)

_validator = None


def get_validator():
    global _validator
    if _validator is None:
        cls_path = get_setting_or_throw("VALIDATOR")
        cls = import_class(cls_path)
        _validator = cls()
    return _validator
