# Handling Playbook Errors

Playbook states can fail for any number of reasons. While SOCless offers many ways to detect failures, one of the easiest approaches is to configure a `TaskFailureHandler` decorator in your playbook.

The `TaskFailureHandler` decorator is a state that is triggered if any other state in the playbook fails. It's typically configured as an Integration state, and can use any integration we desire.

For our `InvestigateLogin` playbook, we'll configure a decorator that uses the HTTPRequest integration to send a failure notice to our #bat-signals channel if any error occurs.

Update our `playbook.json` with the following code

```json hl_lines="33-48"
{
  "Playbook": "[yourname]InvestigateLogin",
  "Comment": "Playbook to investigate an anomalous a login",
  "StartAt": "Geolocate_IP",
  "States": {
    "Geolocate_IP": {
      "Type": "Task",
      "Resource": "${{self:custom.core.HTTPRequest}}",
      "Parameters": {
        "method": "GET",
        "url": "https://freegeoip.app/json/{{context.artifacts.event.details.ip}}"
      },
      "Next": "Send_Notification_To_Slack"
    },
    "Send_Notification_To_Slack": {
      "Type": "Task",
      "Resource": "${{self:custom.core.HTTPRequest}}",
      "Parameters": {
        "method": "POST",
        "url": "https://slack.com/api/chat.postMessage",
        "json": {
          "channel": "#bat-signals",
          "text": "`{{context.artifacts.event.details.username}}` logged in from `{{context.results.Geolocate_IP.json.country_name}}` at coordinates `{{context.results.Geolocate_IP.json.latitude}}`, `{{context.results.Geolocate_IP.json.longitude}}`"
        },
        "headers": {
          "Authorization": "Bearer {{secret('/socless/slack/bot_token')}}"
        }
      },
      "End": true
    }
  },
  "Decorators": {
    "TaskFailureHandler": {
      "Type": "Task",
      "Resource": "${{self:custom.core.HTTPRequest}}",
      "Parameters": {
        "method": "POST",
        "url": "https://slack.com/api/chat.postMessage",
        "json": {
          "channel": "#bat-signals",
          "text": "An error occurred in the our [yourname]InvestigateLogin playbook.\n ExecutionID: {{context.execution_id}} \n Error:\n ```{{context.errors}}```"
        },
        "headers": {
          "Authorization": "Bearer {{secret('/socless/slack/bot_token')}}"
        }
      },
      "End": true
    }
  }
}
```

Notice that our `TaskFailureHandler` configuration looks almost exactly like our `Send_Slack_Message` configuration, but with a different message.

In this case, we're using the handler to notify us of errors in a Slack channel but in reality, this state can be used to perform any activity we'd like to perform if any state in our playbook fails.

Deploy our updates to the SOCless sandbox using:
```
socless stack deploy
```

Then create a file called `error_test.json` in our `functions/tutorial_endpoint` folder with the following payload
```json hl_lines="3 7"
{
  "alert_name": "Suspicious Login Detected",
  "response_plan": "[Yourname]InvestigateLogin",
  "details": [
    {
      "username": "bruce.wayne",
      "ip": "notanip"
    }
  ]
}
```

Finally, test that our decorator works correctly by triggering our endpoint using
```
curl -H "Authorization: $AUTH_TOKEN" \
    -X POST $ENDPOINT_URL \
    -d @functions/tutorial_endpoint/error_test.json
```

If our handler worked correctly, you should have a message in your `#bat-signals` channel indicating that an error occurred.

!!! tip
    While the `TaskFailureHandler` is simple to implement, it isn't the most resilient way to monitor for failures in SOCless. One of its major downsides is that because its also a State in the Playbook, it too can fail.

    Our [Operational Monitoring](../../reference/operational-monitoring.md) reference documentation has more information
    on recommended ways to detect SOCless failures


And that's it! We've successfully added some very basic failure monitoring to our playbook. Feel free to hop into the AWS Step Functions console using `socless auth login --web` to see How SOCless modified our playbook definition based on that state.
