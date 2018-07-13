# This Alexa Session Skill Skill
This example skill demonstrates simple session persistence by ask you
for your favorite color and then remembering that color for the length
of the session.

### This example skill demonstrates the following features:
* logging level setting (debug)
* custom intent
* Amazon intent
* default intent handler
* stack dialog manager
* required fields processing
* voice response (text) with variable content


### Prerequisites
Before starting make sure you have satisfied the prerequisites.
https://dphiggs01.github.io/ask_amy/prerequisites.html

### Deployment

1. Update ``arn:aws:iam::**********:role/alexa_lambda_role`` in cli_config.json.
   Open a terminal window and change into the directory for this skill
    *  ~~~
        $ cd xxxxxxx/ask_amy_example_skills/alexa_session_skill
        $ vim cli_config.json
        ~~~
2. Deploy the code to AWS Lambda
    * Note: Initial deploy should use (create).
        ~~~
        $ ask-amy-cli create_lambda --deploy-json-file cli_config.json
      ~~~
    * Note: Subsequent deploys should use (deploy).
        ~~~
        $ ask-amy-cli deploy_lambda --deploy-json-file cli_config.json
        ~~~
    * Take note of the "FunctionArn": "arn:aws:lambda:us-east-1:**********2273:function:alexa_*****"

3. Create a new skill in your Amazon Development Account.
    * Select `Create Skill` at https://developer.amazon.com/alexa/console/ask

    * Enter a _Skill Name_ and select _custom_ as the skill type. Then select `Create a skill`.

    * Select the `JSON Editor` (Note: the `JSON Editor` is in the left menu pane) Drag & drop the _interaction_model.json_ on to the new skill.
    Click `Save` and `Build Model`.

    * Select `Endpoint` select `AWS Lambda ARN` copy the _Lambda arn_  _arn:aws:lambda:us-east-1:********_
    (Note: It was returned in step two above) to `Default Region` select `Save Endpoint`.

    * Select `Test` tab (Note: `Test` is in the menu bar at the top of the page) on the test page. Select slider to enable test!

**"Congratulations you have deployed a new skill!"**

Note: If you want to check the lambda logs you can use the below
~~~
$ ask-amy-cli logs --log-group-name /aws/lambda/alexa_session_skill
~~~

###### Credit
Many of the example skills were first published as Java or Node.js code
by Amazon https://github.com/amzn. However since Amazon created the _new_
interaction model the original code is no longer available.