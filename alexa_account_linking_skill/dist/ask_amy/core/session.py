import logging

from ask_amy.core.skill_factory import SkillFactory

from ask_amy.core.exceptions import SessionError
from ask_amy.core.object_dictionary import ObjectDictionary
from ask_amy.database.database import DynamoDB

logger = logging.getLogger()


class Session(ObjectDictionary):
    def __init__(self, session_dict):
        super().__init__(session_dict)

        self._persistence = False  # Assume no persistence until explicitlty defined
        config_dict = SkillFactory.load_configuartion(self.__class__.__name__)
        if config_dict:
            self._persistence = self.get_value_from_dict(['persistence'], config_dict)
            if self._persistence:
                self._table_name = self.get_value_from_dict(['tableName'], config_dict)
                self._fields_to_persist = self.get_value_from_dict(['fieldsToPersist'], config_dict)
                if self.get_value_from_dict(['new']):  # if new session load data
                    self.load()

    def session_id(self):
        return self.get_value_from_dict(['sessionId'])

    def application_id(self):
        return self.get_value_from_dict(['application', 'applicationId'])

    def is_new_session(self):
        return self.get_value_from_dict(['new'])

    def user_id(self):
        return self.get_value_from_dict(['user', 'userId'])

    def access_token(self):
        return self.get_value_from_dict(['user', 'accessToken'])

    def consent_token(self):
        return self.get_value_from_dict(['user', 'permissions', 'consentToken'])

    def attributes(self):
        return self.get_value_from_dict(['attributes'])

    def put_attribute(self, name, value):
        logger.debug("**************** entering Session.put_attribute")
        logger.debug("name={} value={}".format(name, value))
        val = value
        obj_dict = self.get_value_from_dict(['attributes'])
        if obj_dict is None:
            self._obj_dict['attributes'] = {}
        try:
            self._obj_dict['attributes'][name] = value
        except KeyError:
            raise SessionError
        return val

    def get_attribute(self, path):
        path.insert(0, 'attributes')
        val = self.get_value_from_dict(path)
        return val

    def load(self):
        logger.debug("**************** entering Session.load")
        if self._persistence:
            user_id = self.user_id()
            dynamo_db = DynamoDB(self._table_name)
            session_data = dynamo_db.load(user_id)
            for name in session_data.keys():
                self.put_attribute(name, session_data[name]['value'])

    def save(self):
        logger.debug("**************** entering Session.save")
        if self._persistence:
            user_id = self.user_id()
            dynamo_db = DynamoDB(self._table_name)
            session_data = self.attributes()
            dynamo_db.save(user_id, self._fields_to_persist, session_data)

    def reset_stored_values(self):
        logger.debug("**************** entering Session.reset_stored_values")
        if self._persistence:
            user_id = self.user_id()
            dynamo_db = DynamoDB(self._table_name)
            dynamo_db.update_data(user_id, DynamoDB.NAME, DynamoDB.SESSION_DATA, "{}")
