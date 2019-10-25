Socless' Human Interaction Workflow enables the incorporation of human input into your playbooks. Using the tools provided by the workflow, Socless developers can create playbooks that interact with users via messaging channels like Slack.

The Human Interaction Workflow is used by configuring an `Interaction` state in a playbook. `Interaction` states are configured the same way as `Task` state, with the difference being that `Interaction` states have their `Type` set to  `Interaction`

The [Human Interaction Architecture](/human-interaction-architecture) documentation provides an in-depth explanation of how human interactions work in Socless and how you can build your own. For now, we'll focus on using Socless Slack (which implements human interaction in Slack) to augment our Getting Started playbook.

Let's start by including functionality to [prompt a user for confirmation](prompting-a-user-for-confirmation.md)
