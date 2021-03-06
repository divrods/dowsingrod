from google.appengine.ext import ndb


class PreferenceEntity(ndb.Model):
    """Persistance model to Appengine NDB datastore for a preference recording"""

    user_id = ndb.StringProperty()  # Session/Vistor Id
    item_id = ndb.StringProperty()  # Id of Artwork/Gallery whatever being recorded
    pref = ndb.BooleanProperty()  # True = Like, #False = Dislike
    timestamp = ndb.DateTimeProperty()  # Timestamp of preference recorded on device

    synced_timestamp = ndb.DateTimeProperty(auto_now_add=True)  # Timestamp when pref synced

    def get_rule_item_id(self):
        # TODO: This is duplicated on the model
        return '%s:%s' % (self.item_id, str(int(self.pref)))


class AssociationRuleEntity(ndb.Model):
    """ Persistance model for association rule """
    ant = ndb.StringProperty(repeated=True)  # antecedent
    con = ndb.StringProperty(repeated=True)  # Confidence
    confidence = ndb.FloatProperty()  # range of [0, 1]
    created_timestamp = ndb.DateTimeProperty(auto_now_add=True)  # Timestamp when pref synced
    rule_key = ndb.StringProperty(indexed=True)  # Searchable/sortable key
    ruleset_id = ndb.StringProperty()  # Resource_id of AssociationRuleSet

    def __repr__(self):
        return "Rule: %s ==> %s , %.3f" % (str(self.ant), str(self.con), self.confidence)


class AssociationRuleSetEntity(ndb.Model):
    """Persistance model to Appengine to Store a association rule set"""
    min_confidence = ndb.FloatProperty()  # range of [0, 1]
    min_support = ndb.FloatProperty()  # range of [0, 1]
    total_rules = ndb.IntegerProperty()
    created_timestamp = ndb.DateTimeProperty(auto_now_add=True)
    is_default = ndb.BooleanProperty()  # Is the default ruleset


class PreferenceTransactionEntity(ndb.Model):
    """
    Persistance Model for storing items preferenced by a user
    """
    rule_item_ids = ndb.StringProperty(repeated=True)
    user_id = ndb.StringProperty(indexed=True)  # Aligns with PreferenceModel.user_id
    total_preferences = ndb.IntegerProperty(indexed=True)
    total_likes = ndb.IntegerProperty(indexed=True)
    total_dislikes = ndb.IntegerProperty(indexed=True)
    created_timestamp = ndb.DateTimeProperty(auto_now_add=True)
    latest_timestamp = ndb.DateTimeProperty(auto_now=True)


class PreferenceItemEntity(ndb.Model):
    """
    Persistance Model for storing usages of an item in preferences
    """
    item_id = ndb.StringProperty(indexed=True)
    user_ids = ndb.StringProperty(repeated=True)
    total_preferences = ndb.IntegerProperty(indexed=True)
    total_likes = ndb.IntegerProperty(indexed=True)
    total_dislikes = ndb.IntegerProperty(indexed=True)
    created_timestamp = ndb.DateTimeProperty(auto_now_add=True)
    latest_timestamp = ndb.DateTimeProperty(auto_now=True)
