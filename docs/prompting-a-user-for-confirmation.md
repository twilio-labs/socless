Open the InvestigateLogin playbook in your socless-playbooks repository. The playbook is at the path `playbooks/investigate_login/playbook.json`

Take a second to review and admire the playbook. Currently, it starts at a `Geolocate_IP` state and ends at a `Notify_Bat_Signals_Channel` state.

Modify `Notify_Bat_Signals_Channel` to transition to a state called `Verify_Login_With_User`. Do with by changing the transition configuration for `Notify_Bat_Signals_Channel` from `"End": true` to `"Next": "Verify_Login_With_User"`.

Next, let's add human interaction into our playbook using the Socless Slack PromptForConfirmation integration and the Socless AwaitMessageResponseActivity receiver. Add the below snippets to the `States` object of your playbook. Note that it doesn't matter the order you add them, as long as the transitions (`Next` fields) are configured correctly.

```
"Verify_Login_With_User": {
          "Type": "Task",
          "Resource": "${{self:custom.slack.PromptForConfirmation}}",
          "Parameters": {
            "target": "$.artifacts.event.details.username",
            "target_type": "user",
            "text": "Hi {context.artifacts.event.details.username}, I noticed that your account was logged into from {context.results.Geolocate_IP.country}",
            "prompt_text": "Did you login from {context.results.Geolocate_IP.country}?",
            "receiver": "Await_User_Verification"
          },
          "Next": "Await_User_Verification"
        },
"Await_User_Verification": {
          "Type": "Task",
          "Resource": "${{self:custom.socless.AwaitMessageResponseActivity}}",
          "Next": "Post_Update_To_Bat_Signals"
        }
```

`Verify_Login_With_User` uses the Lambda Integration, PromptForConfirmation, to send a yes-no button prompt to the user. It accepts the parameters:

- `target`: the Slack entity being messaged
- `target_type`: The type of Slack entity being messaged (in this case, a user)
- `text`: The initial message to
- `prompt_text`: The text that asks as a subject line for the yes-no prompt
- `receiver`: The name of the state in the playbook that will receive the response (in this case Await_User_Verification)

It then immediately transitions to `Await_User_Verifcation` which is the receiver that will capture the users' response. `Await_User_Verification` is also a Task state. However, unlike other Task states, it doesn't rely on a Lambda Integration. Instead, it relies on the Socless `AwaitMessageResponseActivity` which is an AWS Step Functions Activity that receives data from sources external to the playbook -- hence why it doesn't need parameters in its configuration. The `AwaitMessageResponseActivity` receiver concludes the human interaction that was started by the prior state. **Whenever you use an integration that starts a human interaction, you'll need to configure a Task state that uses `AwaitMessageResponseActivity` immediately after the integration to conclude the human interaction**

Our `Await_User_Verification` state transitions to `Post_Update_To_Bat_Signals`. Configure that state to post an update to the #bat-signals channel so we get feedback on the user's response. Do so by adding the below snippet to your state machine

```
"Post_Update_To_Bat_Signals": {
      "Type": "Task",
      "Resource": "${{self:custom.slack.SendMessage}}",
      "Parameters": {
        "target": "bat-signals",
        "target_type": "channel",
        "message_template": "User, `{context.artifacts.event.details.username}` responded `{context.results.Await_User_Verification.actions.value}` to the alert"
      },
      "End": true
    }
```

`Post_Update_To_Bat_Signals` uses the Socless Slack `SendMessage` integration to send a message to the channel. This `SendMessage` integration is identical to the one we created in the [Getting Started tutorial](/your-second-integration-sending-a-slack-Message). We pass it the #bat-signals channel and the templatized message to send. Pay attention to the `{results.Await_User_Verification.actions.value}` variable in the message template. When a Sockless Slack message button is pushed, the result is returned in a dictionary that contains, amongst other things, information about what button was pushed. The information is stored at `*.actions.value` and is the string `"true"` if `yes` was pressed, or `"false"` if `no` was pressed. In the next tutorial, we'll learn how to use that information to guide the execution of our workflow.

For now, let's test our updated playbook to see how it works.


## Testing our updates
Since our playbook has already been listed in our `socless-playbooks` serverless.yml, we simply need to redeploy `socless-playbooks` to publish our updates. Do so by running the below command. Be sure to change `dev` to match the environment you're deploying to (for our tutorials, it should be dev)

```
npm run dev
```

Next, let's send an alert to the [Event Endpoint](/your-first-endpoint) from our Getting Started Tutorial.
The alert payload is below:

```
{
  "alert_name": "Suspicious Login Detected",
  "response_plan": "InvestigateLogin",
  "details": [
    {
      "username": "bruce.wayne",
      "ip": "113.63.125.3"
    }
  ]
}
```

Change the `username` to your Slack username then save the payload to a test_case.json file in the `investigate_login` folder.

Next, use the below curl command to send the payload to our Event Endpoint. Be sure to replace {endpoint-url} with your endpoint URL

```
curl -X POST {endpoint-url} -d @playbooks/investigate_login/test_case.json
```

If the request is successful, you'll receive a notice of an alert in the #bat-signals channel, and a message from the socless-bot asking you if you logged into your account from China. When you click either "yes" or "no" you'll see a new message in the #bat-signals channel with your response.

Congratulations! You've successfully added human interactivity into your playbook! 🍾

Move on to the next page of the tutorial to learn how to control the flow of your playbook based on a human's response
