# The Alex tide Skill

https://github.com/amzn/alexa-skills-kit-java/tree/master/samples/src/main/java/tidepooler



ask-amy-cli create_role --role-name alexa_lambda_role

ask-amy-cli create_template --skill-name alexa_tide_skill  --role-name arn:aws:iam::280056172273:role/alexa_lambda_role --intent-schema-file speech_assets/intent_schema.json

ask-amy-cli create_lambda --deploy-json-file cli_config.json

Any subsequent deploys use this 
ask-amy-cli deploy_lambda --deploy-json-file cli_config.json

ask-amy-cli logs --log-group-name /aws/lambda/alexa_tide_skill 






