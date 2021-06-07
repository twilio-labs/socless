# Creating An Endpoint
Let's get started creating our Endpoint. To spice things up a bit, we'll assume that the system that will send data to our endpoint is a ~~high tech SONAR~~ detection system that will only send alerts in the below structure

=== "Alert our detection system will send"
    ```json hl_lines="7"
    {
        "alert_name": "Anomalous Login IP Detected",
        "details": [{
            "username": "bruce.wayne",
            "ip": "113.63.125.3"
        }],
        "response_plan": "[yourname]InvestigateLogin"
    }
    ```

=== "What our Playbook expects"
    ```json
    --8<-- "docs-snippets/quick-start/playbook_details.json"
    ```

Oh oh. Looks like the fancy detection system is sending the data in a slightly different structure than what we expect. But on the flipside, it's also specifying exactly the `"response_plan"` it wants us to execute, and its requesting our `[yourname]InvestigateLogin` Playbook!

So our endpoint will need to do a number of things:

* Restructure the data to what our Playbook expects,
* Trigger our Playbook,
* Require authentication to ensure only our detection system can trigger it

Thankfully, SOCless provides a helpful function called `create_events` that handles most of the functionality.

The `create_events` function takes two parameters as such: `create_events(event_details, context)`. We don't need to know much about `context` parameter. Our major focus will be on the `event_details` parameter.

`event_details` is expected to be a Python dictionary that has, at minimum, the following fields

```json
{
  "event_type": "Human Readable Name of the Event",
  "playbook": "PlaybookToExecute",
  "event_details": [
    {... #dict of event details},
    {... #dict of event details}
  ]
}
```

When the `create_events` function is called, It triggers one execution of the `playbook` for each `dict of event details`. So in theory, an endpoint can receive a batch of similarly structured events and execute one instance of the playbook per event. For our tutorial though, we only expect one event.

Let's get started implementing our Endpoint to see it all in action.


* First, in our `socless-tutorial-playbook/functions/tutorial_endpoint` folder, create a file called `test_case.json`. Then save the `Alert our detection system will send` contained in the first code block above in the file. **Be sure to update the value for `response_plan` to the name of your actual playbook**

* Next, open our `socless-tutorial-playbook/functions/tutorial_endpoint/lambda_function.py` file and implement the following function. The code comments explain the major parts of the file
```python
# Import create_events function from socless.
from socless import create_events
import json, os


def lambda_handler(event, context):
    try:
        # implement a simple authentication mechanism for our
        # endpoint that checks if the `expected_token`
        # (configured via an `AUTH_TOKEN` environment variable)
        # matches the `provided_token` in the Authorization header
        # of the request
        expected_token = os.environ["AUTH_TOKEN"]
        provided_token = event["headers"]["Authorization"]

        # return 403 error if the provided_token doesn't match
        # the expected_token
        if provided_token != expected_token:
            return {"statusCode": 403, "body": "Invalid authorization token provided"}

        # Construct the `event_details` dict that
        # create_events expects by mapping
        # the values in the alert_payload to
        # their appropriate keys
        # event["body"] contains the alert_payload
        alert_payload = json.loads(event["body"])
        event_details = {
            "event_type": alert_payload["alert_name"],
            "playbook": alert_payload["response_plan"],
            "details": alert_payload["details"],
        }

        # Call create_events with event_details & context
        # to register event and start the playbook
        create_events(event_details, context)
    except Exception as e:
        # return a 400 error if anything above fails
        return {"statusCode": 400, "body": f"{e}"}

    # return 200 statusCode if all is well
    return {"statusCode": 200}
```

That's all the logic we need for our event Endpoint.

***"But waaaaait a second. Our Endpoint needs an `expected_token` to be configured as an `AUTH_TOKEN` environment variable. Don't we need to generate the `expected_token`? Then configure it...somewhere?"***

Correct! Let's do that next.
