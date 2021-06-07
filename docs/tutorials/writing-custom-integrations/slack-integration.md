# Developing our Slack Send Message Integration

Let's create an integration that sends a message to a Slack channel. We'll follow the same steps as before:

* Writing the code for our Integration
* Configuring our integrations dependencies
* Configuring the Integration for Deployment
* Deploying and testing the integration.

## Coding our Slack Send Message Integration

Create a `send_message` folder in our `socless-tutorial-integrations/functions` directory, and include a `lambda_function.py` in that folder.

In the `lambda_function.py`, implement an integration that:

- Expects the following parameters: `text`, `channel`, `bot_token`
- Uses the [Python Slack SDK](https://slack.dev/python-slack-sdk/#) post a message to a Slack channel. [Some Sample Code to help you here](https://slack.dev/python-slack-sdk/web/index.html#messaging)
- Captures the response from Slacks API in a `response` variable and returns `response.data` as its integration output.


Our completed integration should look similar to the below

```python
from socless import socless_bootstrap
from slack_sdk import WebClient


def handle_state(channel, text, bot_token):
    client = WebClient(token=bot_token)
    response = client.chat_postMessage(channel=channel, text=text)
    return response.data


def lambda_handler(event, context):
    return socless_bootstrap(event, context, handle_state)
```


## Configure the slack_sdk Dependency
Our integration relies on the `slack_sdk`. Lets configure it as a deployment dependency.  

This time, however, instead of adding it to our `functions/requirements.txt` file which contains dependencies that should be deployed with every function in the `functions` folder, let's configure our `slack_sdk` to only be deployed with our `send_message` function.

To do so:

- Create a `requirements.txt` file in our `functions/send_message` folder.
- List `slack_sdk` on the first line.

The created file should look like so

```
slack_sdk
```

And our functions folder should now have the below structure

```
functions/
├── requirements.txt
├── geoip
│   └── lambda_function.py
└── send_message
    ├── lambda_function.py
    └── requirements.txt
```

`slack_sdk` is now configured to deploy only with our send_message function as its the only function that needs it. It's good practice to only package dependencies with the functions that need them, as this reduces the size of our deployment package.

Now, let's configure our integration for deployment.


## Configure Our Integration for Deployment
Open the `serverless.yml` file. In the `function` section under our `GeoIP` configuration, configure a `SendMessage` integration that:

- is named `socless_[yourinitial]_tutorial_send_message`
- Has handler `lambda_function.lambda_handler`
- Has the description "Sends a message via Slack"
- Creates its source package from `functions/send_message`

Here's what that our functions section should now look like like:

```yaml hl_lines="10-16"
functions:
  GeoIP:
    name: socless_ubani_tutorial_geoip # Remember to rename this with your initial
    handler: lambda_function.lambda_handler
    description: Integration to geolocate an ip
    package:
      include:
        - functions/geoip

  SendMessage:
    name: socless_[yourname]_tutorial_send_message #replace your initial
    handler: lambda_function.lambda_handler
    description: Send a message using Slack
    package:
      include:
        -  functions/send_message
```

And lastly, configure an `Output` for our `SendMessage` function so that our `resources` section looks like:

```yaml hl_lines="8-11"
resources:
  Outputs:
    GeoIP:
      Description: ARN of GeoIP integration
      Value:
        Fn::Sub: ${GeoIPLambdaFunction.Arn}

    SendMessage:
      Description: ARN of SendMessage Integration
      Value:
        Fn::Sub: ${SendMessageLambdaFunction.Arn}
```

With that, our integration is fully configured and ready for deployment!



## Deploying the Integration
To deploy our integration, execute the following in your terminal in the same directory as the `serverless.yml` file

```
socless stack deploy
```

Once the deployment is complete, you should see the ARN for the Integration's Lambda function displayed. You don't need to note this ARN down as we'll reference it by the `SendMessage` name whenever we need it.

## Testing the Integration
Log into the AWS console using

```
socless auth login --web
```

Then navigate to the Lambda service in your SOCless Sandbox region (us-west-1), and open the Lambda function for the integration we just deployed (`socless_[yourname]_tutorial_send_message`).

Click `Test`, and configure the below test event:
```json
{
  "channel": "#bat-signals",
	"text": "Hello world!",
	"bot_token": "{{secret('/socless/slack/bot_token')}}"
}
```

Save the test event with a name similar to `MySendMessageTest` then execute it.

If it succeeds, we should get a message from our bot in the SOCless bat-signals channel. We should also have an output similar to the below in our AWS Lambda console


```json
{
  "channel": "#bat-signals",
  "text": "Hello world!",
  "bot_token": "{{secret('/socless/slack/bot_token')}}",
  "results": {
    "direct_invoke": {
      "ok": true,
      "channel": "CXXXXXXXX",
      "ts": "160000000.000000",
      "message": {
        "bot_id": "BXXXXXXXX",
        "type": "message",
        "text": "Hello world!",
        "user": "WXXXXXXXX",
        "ts": "160000000.000000",
        "team": "TXXXXXXXS",
        "bot_profile": {
          "id": "BXXXXXXXX",
          "deleted": false,
          "name": "socless_bot",
          "updated": 1000000000,
          "app_id": "AXXXXXXXX",
          "icons": {
            "image_36": "https://avatars.slack-edge.com/2018-07-11/XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX.png",
          },
          "team_id": "TXXXXXXXX"
        }
      }
    }
    }
  }
}
```

Congratulations! We've successfully written a second Integration! :clap:

To wrap up, lets update our `InvestigateLogin` Playbook from our Getting Started Tutorial to use these Integrations.
