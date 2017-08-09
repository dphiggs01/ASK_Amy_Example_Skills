# fact_skill
The fact skill will pick a ramdom facts from the facts.json file and speak it back through Alexa

Only use in a with new development for this example the code is already created
# ask-amy-cli create_template --skill-name alexa_obama_fact_skill --role-name arn:aws:iam::280056172273:role/alexa_lambda_role --intent-schema-file speech_assets/intent_schema.json

It is expected that an AWS role already exists you will need to update the role in the cli_config.json before deploying
ask-amy-cli create_lambda --deploy-json-file cli_config.json

Any subsequent deploys use this 
ask-amy-cli deploy_lambda --deploy-json-file cli_config.json
ask-amy-cli logs --log-group-name /aws/lambda/alexa_obama_fact_skill
