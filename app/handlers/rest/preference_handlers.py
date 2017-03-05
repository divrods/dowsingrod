from rest_core import handlers
from rest_core.resources import Resource
from rest_core.resources import RestField
from rest_core.resources import BooleanField
from rest_core.resources import DatetimeField
from services import preference_service
from models import PreferenceModel

PREFERENCE_FIELDS = [
    # ResourceIdField(output_only=True),
    # ResourceUrlField(resource_url, output_only=True),
    RestField(PreferenceModel.user_id, required=True),
    RestField(PreferenceModel.item_id, required=True),
    BooleanField(PreferenceModel.pref, required=True),
    DatetimeField(PreferenceModel.timestamp),
    DatetimeField(PreferenceModel.synced_timestamp, output_only=True),
]


class PreferenceBaseHandler(handlers.RestHandlerBase):
    """
    Base Handler for Preferences
    """

    def get_rules(self):
        return PREFERENCE_FIELDS

    def get_model_by_id_or_error(self, resource_id):
        """
        """

        return 'DEREERERE'

    def model_to_rest_resource(self, model, verbose=False):
        """Convert a PreferenceModel to a Rest Resource (dict)"""
        return Resource(model, PREFERENCE_FIELDS).to_dict(verbose)


class PreferenceDetailHandler(PreferenceBaseHandler):
    """
    Handler for a single Preference
    """
    def get(self, resource_id):
        pref_model = self.get_model_by_id_or_error(resource_id)
        result = self.model_to_rest_resource(pref_model, True)
        self.serve_success(result)


class PreferenceCollectionHandler(PreferenceBaseHandler):
    """
    Handler for a collection of Preferences
    """

    def get(self):
        models = preference_service.query_preferences()
        return_resources = []
        for pref_model in models:
            return_resources.append(self.model_to_rest_resource(pref_model, True))
        self.serve_success(return_resources)

    def post(self):
        """
        Create a single Preference entity
        """

        model = PreferenceModel(self.cleaned_data.get('user_id'),
                                self.cleaned_data.get('item_id'),
                                self.cleaned_data.get('pref'),
                                self.cleaned_data.get('timestamp'))
        model = preference_service.record_preference(model)  # TODO: This returns a list atm
        self.serve_success(self.model_to_rest_resource(model, True))
        return