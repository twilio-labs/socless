For the final part of our tutorial, let's learn to trigger a [Slack Dialog](https://api.slack.com/dialogs). Slack Dialogs allow humans to provide detailed information to a playbook.

The Socless Slack integration for sending dialogs is called SendDialog. Like PromptForConfirmation, it relies on Socless' human interaction workflow as well, which, as we learned, means it needs to be followed by an AwaitMessageResponseActivity state. In addition, Slack Dialogs have lifecycle requirements that we'll learn about in this tutorial.


The lifecycle for working with a Slack Dialog on any platform is:

* Slack User responds to an interactive message (e.g. button press) or uses a slash command. This generates a trigger_id that is valid for 3 seconds
* Backend system uses trigger_id to open a Slack Dialog for the user. A Slack Dialog can't be opened without the trigger_id that is generated when a user interacts with an interactive message or slash command
* User either submits or cancels the dialog. This sends either a `dialog_submission` or `dialog_cancellation` event back to the backend system.
* Backend system handles either dialog_submission or dialog_cancellation event

When Slack Dialogs are implemented in Socless, the "Backend system" described above is the Socless Playbook. Thus, to use a Slack Dialog in Socless, you need to:

* Send an Interactive Message using PromptForConfirmaton, or request a slash command be run using PromptForResponse Socless Slack Integrations
* Pass the trigger_id that is included in the user's response by Slack to the Socless Slack SendDialog integration, to open the dialog
* Wait for the Users' Dialog Response
* Use a Choice State to check if the user submitted or canceled the dialog
* Handle each response as appropriate.


Let's learn how to implement this by modifying our InvestigateLogin playbook to request additional information -- via a dialog -- when a user specifies that they did **NOT** perform the login we prompted them to confirm.

Start by reconfiguring the `Did_User_Login` Choice state to transition `Request_More_Info` instead of `Reassure_User` when a user responds "no" to our prompt for login verification. Don't delete the `Reassure_User` state, however. We'll still need to reassure the user that help is one the way after we collect more information.

Next, Configure `Request_More_Info` to use our SendDialog integration to request more information as shown below. You can add the configuration anywhere in the States object. Order of states in the States object doesn't matter. All that matters is that transitions are configured correctly.

```
    "Request_More_Info": {
      "Type": "Task",
      "Resource": "${{self:custom.slack.SendDialog}}",
      "Parameters": {
        "receiver": "Await_Additional_Info",
        "trigger_id": "$.results.Await_User_Verification.trigger_id",
        "title": "Tell Us More",
        "elements": [
          {
            "label": "Where and when was your last login to your account?",
            "name": "additional_info",
            "optional": false,
            "placeholder": "My last log in was at ... from ....",
            "type": "text"
          }
        ]
      },
      "Next": "Await_Additional_Info"
    },
    "Await_Additional_Info": {
      "Type": "Task",
      "Resource": "${{self:custom.socless.AwaitMessageResponseActivity}}",
      "Next": "Did_User_Submit_Dialog"
    }
```

SendDialog is configured to follow the Human Interaction Workflow. Pay attention to the parameters passed, specifically trigger_id and elements. trigger_id is sourced from Await_User_Verification -- the state that receives our user's response to the button press. `elements` is built according to Slack's documentation on [authoring Dialog elements](https://api.slack.com/dialogs#elements). Be sure to review that documentation to familiarize yourself with all available Slack Dialog elements. Finally, the state transitions to Await_Additional_Info which will receive the response from the dialog.

The above configuration handles sending a dialog and receiving the response. However, since the response may either be a submission or cancellation, we need a choice state to examine the response and guide our execution. That's what `Did_User_Submit_Dialog` will do. Let's configure that choice state as shown below:

```
"Did_User_Submit_Dialog": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.results.Await_Additional_Info.type",
          "StringEquals": "dialog_submission",
          "Next": "Reassure_User"
        },
        {
          "Variable": "$.results.Await_Additional_Info.type",
          "StringEquals": "dialog_cancellation",
          "Next": "Update_Bat_Signals_Channel"
        }
      ]
    }
```
The state checks the data at `$.results.Await_Additional_Info.type` to determine what action was taken on the dialog i.e. dialog_submission or dialog_cancellation. If the dialog was submitted, it transitions to `Reassure_User` which is already configured in our playbook. If the dialog was cancelled, it transitions to `Update_Bat_Signals_Channel`. Let's configure that state as shown below:

```
"Update_Bat_Signals_Channel": {
      "Type": "Task",
      "Resource": "${{self:custom.slack.SendMessage}}",
      "Parameters": {
        "target": "bat-signals",
        "target_type": "channel",
        "message_template": "User, {context.artifacts.event.details.username}, reported that they did not log into their account but also failed to provide additional details via the dialog. Please investigate."
      },
      "End": true
    }
```
The configuration uses the Socless Slack SendMessage integration to update the bat-signals channel that the dialog requesting additional information wasn't submitted. It then ends the playbook execution.


Deploy the playbook and execute our test case located in the investigate_login folder. Run through all the possible flows of the playbook to get an idea of the user experience. You'll probably identify a number of places where the experience can be improved (e.g. providing a feedback message to the user after they cancel the dialog). Feel free to tackle these improvements to practice what you've learned.


With that addition, you've successfully written a playbook that interacts with a human using message buttons and dialogs! Congratulations 🍾 🍾

That's all for this tutorial series.

In future tutorials, we'll cover:

* Executing Lambda Integrations in Parallel,
* Using Pass States to label branches on your playbook to improve legibility
* Leveraging Socless' Deduplication Mechanism to Handle Duplicate Events
