# Obama Fact Skill
Have Alexa read interesting random facts on any subject of your choosing.
This skill just happens to be about presidential facts. Here is an
interesting fact using ASK Amy this skill is written in less than 25
lines of code!

# Prerequisites
Before starting make sure you have satisfied the prerequisites.
https://dphiggs01.github.io/ask_amy/prerequisites.html

# Deployment

1. Update ``arn:aws:iam::**********:role/alexa_lambda_role`` in cli_config.json.
~~~
$ vim cli_config.json
~~~
2. Deploy the code to AWS Lambda
~~~
$ ask-amy-cli deploy_lambda --create-json-file cli_config.json
~~~
3. Create a new skill in your Amazon Development Account.

**"You are Done!"** *Test*
~~~
$ ask-amy-cli logs --log-group-name /aws/lambda/alexa_obama_fact_skill
~~~

# Alternative Start from scratch
You can also use the ``create_template`` command to create a shell for a new
fact application.
~~~
$ ask-amy-cli create_template --skill-name alexa_obama_fact_skill --role-name arn:aws:iam::280056172273:role/alexa_lambda_role --intent-schema-file speech_assets/intent_schema.json
~~~
