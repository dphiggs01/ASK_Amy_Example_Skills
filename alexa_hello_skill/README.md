# The Alex Hello Skill
This is the simplest skill you can create with ASK_AMY and you do not
even need any code. 

ask-amy-cli create_role --role-name alexa_lambda_role

ask-amy-cli create_template --skill-name alexa_hello_skill --role-name arn:aws:iam::280056172273:role/alexa_lambda_role --intent-schema-file speech_assets/intent_schema.json

ask-amy-cli create_lambda --deploy-json-file cli_config.json

Any subsequent deploys use this 
ask-amy-cli deploy_lambda --deploy-json-file cli_config.json

ask-amy-cli logs --log-group-name /aws/lambda/alexa_hello_skill


Test





