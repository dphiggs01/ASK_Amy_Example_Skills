# fact_skill

ask-amy-cli create_template --skill-name alexa_obama_fact_skill --role-name arn:aws:iam::280056172273:role/alexa_lambda_role --intent-schema-file speech_assets/intent_schema.json

ask-amy-cli create_lambda --deploy-json-file cli_config.json

Any subsequent deploys use this 
ask-amy-cli deploy_lambda --deploy-json-file cli_config.json
