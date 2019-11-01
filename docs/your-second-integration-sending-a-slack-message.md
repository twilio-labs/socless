# Your Second Integration: Send Slack Message
Our second Integration will send a message using Slack. In this tutorial, we'll learn learn how to:

- Setup a Slack Bot for use with Socless
- Store our bots credentials for use with Socless Integrations
- Create an Integration that uses the Slack bot to send messages

This documentation assumes you already have a [Slack instance](https://slack.com) that's ready to use.

# Setting up a Slack bot

Follow the steps below to setup a Slack bot for our tutorial:

1. In a web browser, log into your Slack instance
2. Navigate to https://api.slack.com/apps and hit `Create New App`
3. Enter a name for your application. The tutorial will use `socless-bot`
4. Select your development workspace. It should be the workspace you want your bot to be in
5. Hit Create app
6. On the "Basic Information" page for your app, click "Bots"
7. Click "Add Bot User"
8. Set a display name of your choice. We'll use `socless-bot`
9. Set a default username for your bot. We'll use `socless-bot`
10. Set "Always Show My Bot as Online" to "On"
11. Click "Add Bot User" again to save the changes
12. In the left sidebar, select "Oauth & Permissions"
13. Click "Install App to Workspace". Click "Authorize" to add the bot to your Slack Workspace
14. Once authorization is complete, you will be redirected back to the "Oauth & Permissions" page which will now display a "Bot User OAuth Access Token". Note this token down. Our integration will need this token
15. Log into your Slack instance in the Slack app. Click "Direct Messages" in the sidebar and search for your bot. Your bot should show up, ready for action.
16. Create a public channel in your Slack instance called "bat-signals". We'll need it for the rest of our tutorial.
17. Invite your Slack bot to the #bat-signals channel so that it can send messages to it

# Storing our Bots Credential for Use in Socless
The current recommendation for storing credentials for use in the Socless Framework is to use the AWS Systems Manager (SSM) Parameter Store service.

To store the bot token in SSM Parameter Store:

1. Log into your AWS Account in the your Socless dev region and navigate to AWS Systems Manager
2. In the left sidebar of the Systems Manager page, select Parameters Store (you may need to scroll to see it)
3. On the Parameter Store page, click "Create Parameter"
4. Name your parameter /socless/slack/bot_token
5. Add a description for the parameter. We'll go with "Access token for Socless Slack bot"
6. Under `Type`, select SecureString.
7. Under KMS Key ID select `alias/socless/lambdaKmsKey`
8. Under value, paste the `Bot User OAuth Access Token`
9. Click "Create Parameter"

Your bot token should now be encrypted and saved in AWS SSM Parameter Store under the name `/socless/slack/bot_token`. We'll specify that name in our serverless.yml file when we're configuring our integration for deployment

We're now set to write our Slack 'Send Message' Integration

# Writing our Slack 'Send Message' Integration
## Coding the integration
Create a `send_message` folder in our `socless-tutorial/functions` directory, and include a `lambda_function.py` in that folder.

In `lambda_function.py`, implement an integration that:

- Fetches the Slack bot token from its environment variables.
- Has a `handle_state` function with parameters `context`, `target`, `target_type`, `message_template` where the logic to send a Slack message is implemented.
- Determines the appropriate Slack ID to send the message to depending the `target_type`  `user` or `channel`
- Invokes the `socless_template_string` library function to render the `message_template` using the playbook `context`
- Uses the Slack `chat.postMessage` api to send the message and returns the resulting response from the Slack API in a dictionary
- Has a `lambda_handler` entry function that invokes `socless_bootstrap` to manage its life-cycle with the `include_event` parameter set to `True` so that all data from the playbook execution is made available to the integration (we'll need it data to render our message template)

Here's our implementation for the integration
```
import slack, os
from socless import socless_bootstrap, socless_template_string

SOCLESS_BOT_TOKEN = os.environ.get('SOCLESS_BOT_TOKEN')
sc = slack.WebClient(token=SOCLESS_BOT_TOKEN)

def find_user(name, page_limit=100, include_locale='false'):
    """
    Find a user's Slack profile based on their full or display name
    """
    paginate = True
    next_cursor = ''
    while paginate:
        resp = sc.users_list(cursor=next_cursor, limit=page_limit, include_locale=include_locale)
        data = resp.data
        next_cursor = resp.data['response_metadata'].get('next_cursor','')
        if not next_cursor:
            paginate = False

        for user in data['members']:
            user_names = [user.get('name'), user.get('real_name'), user.get('profile',{}).get('real_name')]
            if name in user_names:
                return {"found":True, "user": user}

    return {"found": False}


def handle_state(context, target, target_type, message_template):
    """
    Send a Slack message to either a user or channel
    """
    target_id = ''
    # Determine Slack ID for the target
    if target_type == 'user':
        result = find_user(target)
        if result['found'] == False:
            raise Exception(f"User {target} not found in Slack instance")

        target_id = result['user']['id']
    else:
        target_id = f"#{target}"

    # Render the message template and send the message
    message = socless_template_string(message_template, context)
    resp = sc.chat_postMessage(channel=target_id, text=message, as_user=True)
    return resp.data

def lambda_handler(event,lambda_context):
    return socless_bootstrap(event,lambda_context,handle_state, include_event=True)
```

## Specifying Dependencies
Our integration relies on the Python slackclient library which isn't available on AWS Lambda by default. To specify that our dependency be included with our deployment package, create a `requirements.txt` file in the `send_message` folder and add `slackclient` to the first line. Because this requirements.txt exists within the send_message folder, `slackclient` will only be included in the package for the `send_message` function.

## Configuring Our Integration for Deployment
Open the `serverless.yml` file. First, in the `function` section, include a configuration for our integration that:

- is referenceable as `SendMessage`
- named `socless_tutorial_send_message` in AWS Lambda
- Has handler `lambda_function.lambda_handler`
- Has the description "Sends a message via Slack"
- Creates its source package from `functions/send_message`
- Has environment variable `SOCLESS_BOT_TOKEN` which references the Slack bot token we saved in SSM as `socless/slack/bot_token`
Here's what that configuration looks like:
```
SendMessage:
    name: socless_tutorial_send_message
    handler: lambda_function.lambda_handler
    description: Send a message using Slack
    package:
      include:
        -  functions/send_message
    environment:
      SOCLESS_BOT_TOKEN: ${{ssm:/socless/slack/bot_token~true}}
```
Ensure the configuration starts at one-indentiation level under the `functions` section. This configuration will deploy a Lambda function and Cloudwatch Log Group that are referenceable as `SendMessagelambdaFunction` and `SendMessageLogGroup` respectively.

Next, in the resources Output section, expose the ARN of the Lambda function using the configuration below so that it can be referenced by playbooks

```
SendMessage:
      Description: ARN of SendMessage Integration
      Value:
        Fn::Sub: ${SendMessageLambdaFunction.Arn}
```
With that, our integration is fully configured and ready for deployment
## Deploying the integration
Activate your Python 3 virtual environment (if it is no longer active), and run the below command within the socless-tutorial directory
```
npm run dev
```
Once the deployment is complete, you should see the ARN for the integration's Lambda function displayed. You don't need to note this ARN down as we'll reference it by the `SendMessage` name whenever we need it

# Testing the Integration
Log into the AWS Console, navigate to the Lambda service in your Socless dev region and open the `socless_tutorial_send_message` intgration which we just deployed.

Configure the below test event which sends a "hello world" message to the `bat-signals` channel which we created and added our bot to earlier in the tutorial

```
{
  "_testing": true,
  "State_Config": {
    "Name": "Test_State",
    "Parameters": {
      "target": "bat-signals",
      "target_type": "channel",
      "message_template": "Hello, world!"
    }
  }
}
```
Save and execute the test case, You should get a "Hello, world!" message from the bot in the bat-signals channel.

Now, let's configure a second test case that's much more representative of how we'd use our integration in a full-fledged playbook. It includes an `artifacts` object which simulates information about the alert that triggered the playbook that calls our integration.

```
{
    "_testing": true,
    "artifacts": {
        "event": {
            "details": {
                "distress_channel": "bat-signals",
                "distressed_user": "Commissioner Gordon"
            }
        }
    },
    "State_Config": {
        "Name": "Test_State",
        "Parameters": {
            "target": "$.artifacts.event.details.distress_channel",
            "target_type": "channel",
            "message_template": "The Bat Signal was turned on by {context.artifacts.event.details.distressed_user}"
        }
    }
}
```

Save the test case and execute the function. You should receive a message in the bat-signals channel that reads "The Bat Signal was turned on by Commissioner Gordon".

However, as you can see from our `Parameters` config, neither the "bat-signals" channel nor "Commissioner Gordon" were explicitly passed to the `target` or `message_template` parameters. Instead, those values were passed using a Parameter reference (with format `$.*`) and a template variable (format `{context.*}` ) respectively that referenced the parts of our artifacts object that contained the information we needed. You can learn all about parameter references and template variables in the [Parameter References & Template Variables](parameter-references-and-template-variables.md) documentation, or you can keep following the tutorial to learn as you go.



# Conclusion
We've created our second integration! :champagne:

In doing so we've:

- Learned how to store credentials and AWS SSM Parameter Store for use with Socless Integrations
- How to pass those parameters to our integration via an `environment` variable configuration
- Gotten a very brief intro to [Parameter References & Template Variables](parameter-references-and-template-variables.md)

With both integrations created, we're ready to write our first playbook. Head to the next page to begin
