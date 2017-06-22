from ask_amy.tests.utility import TestCaseASKAmy
from ask_amy.database.database import DynamoDB
from botocore.exceptions import ClientError
import json


class DynamoDBTest(TestCaseASKAmy):
    def setUp(self):
        self.dynamo_db = DynamoDB("Bolus", "http://localhost:8000")

    def test_new_session_started(self):
        try:
            self.dynamo_db.create_table()
            print("Table created")
        except ClientError as e:
            print(e.response['Error']['Message'])
            print("Table already exists")

    def test_update_data(self):
        print("test_update_data")
        user_id = '1234'
        name = 'key'
        attribute = 'dialog_fields'
        persitent_data = {
                 'target_bg_level_day': {'value': '100'},
                 'target_bg_level_night': {'value': '150'},
                 'correction_factor_day': {'value': '30'},
                 'correction_factor_night': {'value': '35'},
                 'breakfast_carb_ratio': {'value': '6'},
                 'lunch_carb_ratio': {'value': '8'},
                 'dinner_carb_ratio': {'value': '10'}
                }

        response = self.dynamo_db.update_data(user_id, name, attribute, str(persitent_data))
        print(response)
        # print(self.dynamo_db.get_item(user_id, name))

    def test_get_item(self):
        print("test_update_data")
        user_id = '1234'
        name = 'key'
        attribute = 'dialog_fields'
        item = self.dynamo_db.get_item(user_id, name)
        print(type(item))
        print(item)
        for key in item.keys():
            print("key={} value={}".format(key, item[key]))
        conversation_data = eval(item[attribute])

        print("item correction_factor_day={}".format(conversation_data['correction_factor_day']))

    def test_query_by_userid(self):
        print("test_query_by_userid")
        user_id = '1234'
        results = self.dynamo_db.query_by_userid(user_id)
        print(type(results))
        print(len(results))
        user_data = results[0]
        # print(user_data['dialog_fields'])
        print(json.dumps(user_data['dialog_fields'], indent=4))

    def test_delete_item(self):
        print("test_delete_item")
        user_id = '1234'
        name = 'key'
        results = self.dynamo_db.delete_item(user_id, name)
        print(results)
        # return_val = json.dumps(response['Item'], indent=4, cls=DecimalEncoder)
