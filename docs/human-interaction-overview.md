Socless' Human Interaction Workflow enables the incorporation of human input into your playbooks. Using the tools provided by the workflow, Socless developers can create playbooks that interact with users via messaging channels like Slack.

To use the Human Interaction Workflow, two Task states must be configured in a playbook:

1. One that sends out a message to a user using a Lambda Integration that starts a human interaction
2. Another that returns the users' response to the playbook using Socless' `AwaitMessageResponseActivity` resource

**The states must be configured in the sequence described above, i.e. the state that sends the message using an integration must immediately transition to a state that uses the `AwaitMessageResponseActivity` state to receive the user's response**

The diagram below shows the Human Interaction Workflow in use in a playbook

[diagram coming soon]

The `AwaitMessageResponseActivity` is simply an [AWS Step Function's Activity](https://docs.aws.amazon.com/step-functions/latest/dg/concepts-activities.html) that pauses a playbook's execution until the user's response is returned to the playbook. A simplified way to think of it is as a receiver for a message coming into a playbook. As such, we'll refer to it as the AwaitMessageResponseActivity receiver during the course of our tutorial

The [Human Interaction Architecture](/human-interaction-architecture) documentation provides an in-depth explanation of how human interactions work in Socless and how you can build your own. For now, we'll focus on using Socless Slack (which implements human interaction in Slack) to augment our Getting Started playbook.

Let's start by including functionality to [prompt a user for confirmation](prompting-a-user-for-confirmation.md)
