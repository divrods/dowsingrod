"""
Preference Service

Please keep the service layer agnostic to persistance layer (api) or communication layer (handlers)
"""
from services import item_service
from services import transaction_service
from api import preference_api


def get_by_id(id):
    return preference_api.get_model_by_id(id)


def record_preference(preference_models):
    """"
    Method to persist a preference or list of preferences

    Note: If a single PreferenceModel instance is given, returns a single
        PreferenceModel instance
    """

    is_single = False
    if not isinstance(preference_models, list):
        is_single = True
        preference_models = [preference_models]

    # Iterate over all the persistance models and convert to ndb models
    preference_models = preference_api.create_multi(preference_models)

    # Update item histogram  # TODO: Perhaps do this in a deferred task
    item_service.update_item(preference_models)
    transaction_service.update_transaction(preference_models)

    if (is_single):
        return preference_models[0]
    return preference_models


def query_preferences(*args, **kwargs):
    """
    Query for a set of preferences models
    :returns 3-tuple (models, cursor, more)
    """

    return preference_api.query_preference_models(*args, **kwargs)
