# account link demo skill

* Create a simple application.
We will use the hello world skill
1. Developer console create
    copy intent model
    copy utterances

2. create the skills pyhton implementation

class AccountLinkDialog(DefaultDialog):

    def account_link_intent(self, method_name=None):
        """
        Called to generate an Obama fact
        """
        return self.handle_default_intent(method_name)


3. create a skill_configuration.json

set className
set intent


4. run manage_lambda_function.sh
this will crreate the lambda function
copy the arn paste it into the enpoint of the skill

5. test


* Once complete go back to the  configuration

Authorization URL: https://www.amazon.com/ap/oa
client ID: amzn1.application-oa2-client.87b4d880dxxxxxxxx
scope: postal_code
Access token uri: https://api.amazon.com/auth/o2/token
client secret: copy from client secret in security profile




ask-amy-cli create_role --role-name alexa_lambda_role

ask-amy-cli create_template --skill-name alexa_account_linking_skill --role-name arn:aws:iam::280056172273:role/alexa_lambda_role --intent-schema-file speech_assets/intent_schema.json

ask-amy-cli create_lambda --deploy-json-file cli_config.json

Any subsequent deploys use this 
ask-amy-cli deploy_lambda --deploy-json-file cli_config.json

ask-amy-cli logs --log-group-name /aws/lambda/alexa_account_linking_skill


  
