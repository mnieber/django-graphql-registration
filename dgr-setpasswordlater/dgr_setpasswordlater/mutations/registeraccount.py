import django_graphql_registration.mutations as mutations
import graphene
from dgr_setpasswordlater.mutations.utils import extract_token
from django_graphql_registration.utils.get_backend import get_backend
from django_graphql_registration.utils.get_setting_or import get_setting_or


class RegisterAccount(mutations.RegisterAccount):
    class Arguments:
        email = graphene.String()
        accepts_terms = graphene.Boolean()
        terms_version_accepted = graphene.String(
            required=False, default_value=get_setting_or("1.0.0", "TERMS_VERSION")
        )

    activation_token = graphene.String()

    @classmethod
    def run(cls, errors, **kwargs):
        result = get_backend().register_account(errors, **kwargs)

        return_email_already_taken = get_setting_or(True, "RETURN_EMAIL_ALREADY_TAKEN")
        if not return_email_already_taken and "ALREADY_TAKEN" in errors["email"]:
            errors["email"].remove("ALREADY_TAKEN")

        return result

    @classmethod
    def extract_output_params(cls, result):
        return {"activation_token": extract_token(result, "activation_token")}
