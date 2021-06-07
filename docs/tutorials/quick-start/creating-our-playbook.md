# Developing our InvestigateLogin Playbook
In this tutorial, we'll be implementing the `InvestigateLogin` playbook we discussed in the introduction. Here's the event we expect to trigger our Playbook

=== "Our Expected Event"
    ```json
    --8<-- "docs-snippets/quick-start/playbook_details.json"
    ```

=== "Playbook Execution Context it'll generate"
    ```json
    --8<-- "docs-snippets/quick-start/playbook_initial_context.json"
    ```



To investigate this, our Playbook will geolocate the IP address and send the information to a slack channel called `#bat-signals`.


For IP Geolocation, we'll use the [Freegeoip API](https://freegeoip.app) because its free!

We can test the output of the Freegeoip API by running the below `curl` command in our terminal

```bash
curl --request GET --url https://freegeoip.app/json/113.63.125.3
```

To send a Slack message, we'll use the [Slack's PostMessage API](https://api.slack.com/methods/chat.postMessage)

To integrate with these APIs, we'll be using SOCless' built-in [HTTPRequest Integration](../../reference/builtin-integrations/http_request.md). The HTTPRequest Integration enables us construct arbitrary HTTP requests to any url. You can think of it as SOCless' version of the `curl` command we used above. And if you have experience with the [Python Requests library](https://docs.python-requests.org/en/master/), you'll feel right at home with it because the integration uses Python Requests internally and follows its [request syntax](https://docs.python-requests.org/en/latest/api/#requests.request) (albeit having some additional parameters that are specific to SOCless).

To get started, let's configure our `Geolocate_IP` state

!!! tip "Naming States"
    SOCless States are expected to be named according to the `Uppercase_Underscore` notation

    We recommend starting their names with Verbs (e.g `Geolocate_IP`) not Nouns `IP_Geolocation` as we find it makes it easier to read and describe our workflows to others

## Configuring our Geolocate_IP State

Open the `playbook.json` file located in the `playbooks/investigate_login` folder of our `socless-tutorial-playbook` repository and:

* Name our **Playbook**, `[yourname]InvestigateLogin`
* Give it the **Comment** `"Playbook to investigate an anomalous a login"`
* Ensure the **StartAt** is `Geolocate_IP`
* Configure our **Geolocate_IP** state by
    * Setting its **Type** set to `Task` since it will use an Integration
    * Setting its **Resource** to `${{self:custom.core.HTTPRequest}}`, indicating that its using the HTTPRequest integration
    * Instructing the integration, via our **Parameters**, to make a request to the **url** `"https://freegeoip.app/json/{{context.artifacts.event.details.ip}}"` using the `GET` http **method**
    * Finally, lets set our **Next** state to `Send_Notification_To_Slack`

Our final output should be

```json hl_lines="2 11"
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
    }
  }
}
```

--8<-- "docs-snippets/replace_yourname.md"

We've just configured our first SOCless Playbook state!

Before we move on, let's observe that instead of hardcoding the ip `113.63.125.3` in our **url** above, we referenced it from our Playbook Execution Context using `{{context.artifacts.event.details.ip}}`. `{{context.artifacts.event.details.ip}}` is a [Template Variable](../../reference/variables.md#template-variables).


!!! info "Template Variables Explained"
    Template Variables are how we specify dynamic data in our playbook. They are defined using the `{{ }}` syntax, and they bring many powerful features to SOCless. The `{{context.*}}` Template Variable enables us to pass any data that exists in the Playbook Execution Context as a `Parameter`.

    In the next section, we'll see another Template Variable that enables us securly pass a credential from SOCless secret store as a parameter.

    You can also refer to our [Template Variable](../../reference/variables.md#template-variables) reference documentation to learn more about them


!!! info
    Your keen eyes may be looking at the `Resource` value, `${{self:custom.core.HTTPRequest}}` and wondering what it is. It is **NOT** a Template Variable. It's another a type of variable called a [Serverless Variable](../../reference/variables.md#serverless-variables). We'll cover it in detail our [Developing Custom Integrations](../writing-custom-integrations/introduction.md) tutorial!

Let's get started on our `Send_Notification_To_Slack` state

## Configuring Our `Send_Notification_To_Slack` State

For our `Send_Notification_To_Slack` state, we want to send the `country_name`, `latitude` and `longitude` of our geolocated IP as well as additional text for context to a Slack channel called #bat-signals

To help us get started here's a refresher of what we expect our `Playbook Execution Context` to look like **after** the `Geolocate_IP` state executes

=== "Expected Playbook Execution Context after Geolocate_IP executes"
    ```json hl_lines="10-25"
    --8<-- "docs-snippets/quick-start/playbook_after_geolocate.json"
    ```

Let's go ahead and configure our `Send_Notification_To_Slack` state in our `playbook.json`. It'll be a `Task` state that uses the `HTTPRequest` integration just like our `Geolocate_IP` state did. However, for our `Parameters`:

* We'll make a `POST` **method** request to the **url** `https://slack.com/api/chat.postMessage`
* Since Slack's chat.postMessage API expects an `application/json` payload containing the `text` and `channel` information, we'll configure a **json** field with an object that has:
    * **channel** set to `#bat-signals`
    * **text** set to
    ```
    "`{{context.artifacts.event.details.username}}` logged in from `{{context.results.Geolocate_IP.json.country_name}}` at coordinates `{{context.results.Geolocate_IP.json.latitude}}`, `{{context.results.Geolocate_IP.json.longitude}}`"
    ```
* Since Slack also expects an `Authorization` header that contains a `Bearer [token]`, we'll add a **headers** field that's also a JSON object. It will have an `Authorization` field with its value set to `Bearer {{secret('/socless/slack/bot_token')}}`
* Lastly, instead of configuring a `Next` field for our `State` -- we don't have one as this is the last state of our playbook -- we'll mark this state as our end state by setting an **End** field to `true`

!!! info "Hey Look! It's another Template Variable!"
    The `{{secret('')}}` Template Variable enables us pass a `secret` (i.e. credential) from SOCless' Secret Store as a `Parameter` without hard-coding the secret in our Playbook. And because Integrations are responsible for resolving Template Variables at runtime, our secret won't be exposed during the Playbook deployment process either! This helps us keep secrets out of any code repositories or build systems we use to store and deploy our playbooks!

     In our case above, we're referencing the secret named `'/socless/slack/bot_token'` (Note: this secret was added by your SOCless administrator). The single quotes (`''`) are very important when using the `{{secret('')}}` Template Variable because it tells SOCless that the text between the quotes should be treated as literal strings, not dynamic data.


!!! info
    All `Task` type states must either transition to a `Next` state or be an `End` state.


Our updated `playbook.json` should now look like this

```json hl_lines="14-30"
{
  "Playbook": "[Yourname]InvestigateLogin",
  "Comment": "Playbook to investigate a login",
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
  }
}
```

!!! tip
    You might need to horizontal-scroll in the code block to view the full sample


And that's it! We've finished writing our Playbook!

Before we move on to deploying, take a moment to review how we used Template Variables in the `text` field to reference the `latitude`, `longitude`, and `country_name` that we expect will be added to the Playbook Execution Context after the `Geolocate_IP` state executes. Feel free to compare them to the "Expected Playbook Execution Context after Geolocate_IP executes" which we posted above. Once you're satisfied with your understanding, congratulate yourself! We've just learned how to pass the output from one state as Parameters to another!


Let's head to the next section to learn how to deploy and test our Playbook.


!!! tip
    **Before moving to the next section, confirm that the #bat-signals Slack channel has been created and our Slackbot has been added to it**
