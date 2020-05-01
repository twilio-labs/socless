Robust response plans are seldom linear; seasoned responders expect their actions and investigations to generate new insights that require a slight change of tactics. Courtesy of AWS Step Functions, Socless is equipped with [Choice States](https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-choice-state.html) that allow playbooks to choose the right path of execution based on the results of a prior action. In this tutorial, we'll learn how to configure a Choice state in a playbook. Specifically, we'll configure our playbook to:

- Thank the user if they indicate they performed the login by clicking "yes", **OR**
- Inform the user that help is on the way if they weren't responsible for the login

Start by removing the `Post_Update_To_Bat_Signals` state from the investigate_login Playbook. Delete both the state name and configuration object.

Then, change the `Next` transition of the `Verify_Login_With_User` state to `Did_User_Login`. `Did_User_Login` will be the name of our `Choice` state.

Configure `Did_User_Login` as shown below. We'll talk through the config in a moment

```
"Did_User_Login": {
      "Type": "Choice",
      "Choices": [
        {
          "Variable": "$.results.Verify_Login_With_User.actions.value",
          "StringEquals": "true",
          "Next": "Thank_User"
        },
        {
          "Variable": "$.results.Verify_Login_With_User.actions.value",
          "StringEquals": "false",
          "Next": "Reassure_User"
        }
      ]
    }
```

Since `Did_User_Login` is a Choice state, the `Type` is set to `Choice`. The primary configurable for a Choice state is a list of `Choices`. Each item in the list is an object that represents a Choice rule; a condition to be evaluated and selected if true. Each Choice Rule consists of three components: a variable --contained within our Playbook Context Object-- to evaluate, the comparison to perform, and the state to transition to if the comparison evaluates to `True`.

The 'Variable' the Choice state checks against is specified using a Parameter Reference -- exactly the way you'd pass a parameter to an Integration. **However, unlike an Integration, A Choice State can only reference parameters from the immediately preceding state i.e the state that transitioned to it. You can learn more about that in the [State Management In Socless documentation](state-management-in-socless.md)**. For now, the key thing to remember is that Choice states need to be configured after the state that generates the data being evaluated.

The Comparison expresses the type of check to perform against the 'Variable'. Choice Rules support different types of comparisons such as `StringEquals`, `BooleanEquals`, `NumericEquals` and more. For a full list of the supported comparisons, refer to the [AWS Step Functions Choice State documentation](https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-choice-state.html)

Finally, the 'Next' transition functions exactly as it does in Integrations.

The Choice Rules in the Choices list are evaluated in order. The first choice that evaluates to true determines what state the playbook will be transitioned to next.

The above Choice Rules checks the variable `$.results.Verify_Login_With_User.actions.value` to see if it is a string that's either equal to "yes" or "no". If the string is equal to "yes", the Choice state transitions to the `Thank_User` state. If it's "no", it transitions to the `Reassure_User` state. Let's go ahead and configure both states.

Both `Thank_User` and `Reassure_User` will use the Socless Slack SendMessage integration to message the user based on their response. Here are their configurations:

```
    "Thank_User": {
      "Type": "Task",
      "Resource": "${{self:custom.slack.SendMessage}}",
      "Parameters": {
        "target": "$.artifacts.event.details.username",
        "target_type": "user",
        "message_template": "Thanks for the confirmation! I'll let the security team know everything is fine"
      },
      "End": true
    },
    "Reassure_User": {
      "Type": "Task",
      "Resource": "${{self:custom.slack.SendMessage}}",
      "Parameters": {
        "target": "$.artifacts.event.details.username",
        "target_type": "user",
        "message_template": "Oh oh. Seems like something is amiss here. I'll inform the security team immediately"
      },
      "End": true
    }
```

Once you've included these configurations in your States object, redeploy the playbook then test it again.
After answering the message prompt you receive, you'll receive another Slack message that differs based on the response you selected. Be sure to test both parts in your execution.

And that's it. You've successfully configured a choice state in your playbook.
Let's move on to the next tutorial and learn how to [Collect Information using a Slack Dialog](collect-information-using-a-slack-dialog.md)
