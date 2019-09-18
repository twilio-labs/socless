# Your First Endpoint
Socless uses Event Endpoints to receive event/alert data from external systems and trigger playbooks.

At their core, Event Endpoints are simply AWS Lambda functions that invoke the `create_events` function from the `socless` Python library with the information necessary to register the event within Socless and trigger the appropriate playbook. As such, the bare-bones, psuedo-code implementation for any Socless Event Endpoint looks like this:

```
from socless import create_events

def lambda_handler(event, context):
    # Populate event_details object with approriate fields
    event_details = {
        'event_type': '...', # event name
        'playbook': '...',  # playbook name
        'details': [{'...'},{'...'}] # alert findings
    }
    # Invoke create_events function with event_details
    create_events(event_details, context)
    return {"statusCode": 200}
```

The `create_events` function takes two parameters: `event_details` and `context`.

`context` is the AWS Lambda context which all Lambda functions receive when they are executed by AWS. It’s passed to the create_events function without any modification.

`event_details` is a dictionary constructed by the developer of the Event Endpoint that must contain the below key-value pairs:

| *Key*        | *Type*          | *Description*                                                            | *Required?* | *Example Value*                                      |
|------------|---------------|------------------------------------------------------------------------|-----------|----------------------------------------------------|
| event_type | string        | The unique event name                                                  | Yes       | Anomalous Login IP Detected                        |
| details    | list of dicts | List of dictionaries containing aggregated findings for the event type | Yes       | [{"username": "bruce.wayne","ip": "113.63.125.3"}] |
| playbook   | string        | The Playbook to execute for the event                                  | Yes       | InvestigateLogin                                   |

For our tutorial, all the values needed to populate the `event_details` dictionary are conveniently contained in the alert payload our detection system will send.

So the implementation for our tutorial endpoint will look like this:
```
from socless import create_events
import json

def lambda_handler(event, context):
    alert_payload  = json.loads(event['body'])
    event_details = {
        'event_type': alert_payload['alert_name'],
        'playbook': alert_payload['response_plan'],
        'details': alert_payload['details']
    }
    try:
        create_events(event_details, context)
    except Exception as e:
        return {"statusCode": 400, "body": f"{e}"}
    return {"statusCode": 200}
```

Include this implementation in the `lambda_function.py` file in the `tutorial_endpoint` folder. Note that the current implementation does not include an authentication mechanism to protect our endpoint. Authentication for endpoints will be discussed in the Event Endpoints reference documentation here. For now, we’ll keep our endpoint simple and include authentication later in our tutorial.

With the logic for our Event Endpoint implemented, we’re ready to configure it for deployment
# Configuring our Event Endpoint for Deployment
Much like Socless’ core infrastructure, Event Endpoints are deployed as Serverless Framework applications. Since we created our `socless-tutorial` folder using the `socless-integrations-template`, it is already pre-configured with much of the information we need to deploy our Event Endpoint (the current pre-configurations will be explained in the `socless-integrations-template` reference documentation here).

All we need do now is add configurations for the `tutorial_endpoint` function we just created.
Open the `serverless.yml` file contained within our `socless-tutorial` folder. This file is where configurations for our `socless-tutorial` Serverless application lives. *At the bottom of the file*, let’s configure a lambda function that:

* is reference-able in our config as `TutorialEndpoint`
* is named `_socless_tutorial_endpoint`
* has its entry point (handler) at `lambda_function.lambda_handler`
* has the description: “Receives alerts from our tutorial detection system”
* creates its source package from the contents of the `functions/tutorial_endpoint` folder of our `socless-tutorial` folder
* is triggered by an http POST request to the `/endpoints/tutorial` path of Socless’ API endpoint

Here’s what that configuration looks like:
```
  TutorialEndpoint:
    name: _socless_tutorial_endpoint
    handler: lambda_function.lambda_handler
    description: Receives alerts from our tutorial detection system
    package:
      include:
        - functions/tutorial_endpoint
    events:
      - http:
          path: /tutorial
          method: post
```

We are now ready to deploy and test our endpoint.
# Deploy The Endpoint
Since we’re still in the development phase, we’ll only deploy the event endpoint to our Socless dev environment. Do so by running the below command
```
npm run dev
```
Once the deployment is successful, you will find a URL that ends in `/tutorial` in the *Service Information* section. This is the URL for the endpoint we just deployed. It’s where our tutorial detection system will send our alert payload. Keep it handy. We'll need it to [test the playbook](./Test-Your-First-Playbook)
