# The Alex High Low Guessing game
This is the simplest guessing game skill. This skill demonstrates automatic persistence

You will need to make sure that you have a valid role in you cli_config.json
ask-amy-cli create_lambda --deploy-json-file cli_config.json

Any subsequent deploys use this 
ask-amy-cli deploy_lambda --deploy-json-file cli_config.json

ask-amy-cli logs --log-group-name /aws/lambda/alexa_high_low_skill




