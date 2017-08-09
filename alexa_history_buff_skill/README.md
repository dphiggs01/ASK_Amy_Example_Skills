# The Alex History buff
This skill calls Wikipedia to get history info about a specific day in history

ask-amy-cli create_role --role-name alexa_lambda_role

The create_template is not needed unless you would like to build this skill from scratch
# ask-amy-cli create_template --skill-name alexa_history_buff_skill --role-name arn:aws:iam::280056172273:role/alexa_lambda_role --intent-schema-file speech_assets/intent_schema.json

Make sure that the AWS Role is in sync with your AWS environment
ask-amy-cli create_lambda --deploy-json-file cli_config.json

Any subsequent deploys use this 
ask-amy-cli deploy_lambda --deploy-json-file cli_config.json

For debugging you can easily list the log output
ask-amy-cli logs --log-group-name /aws/lambda/alexa_history_buff_skill




