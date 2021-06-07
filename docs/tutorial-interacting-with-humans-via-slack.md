This tutorial expands on the [Getting Started Tutorial](getting-started.md) to introduce you to more advanced playbook development concepts. Specifically, you'll learn how to:

* Interact with humans using Socless' Human Interaction Workflow and Slack Integrations
* Add branching logic to our State Machine using Choice
* Make our playbooks more legible using Pass States

In our Getting Started Tutorial, we wrote a playbook called "Investigate Login" that handled a "Suspicious Login" alert by:

1. Geolocating the Login IP to identify its country, latitude, and longitude
2. Posting a message containing that information to a #bat-signals channel in Slack

In this tutorial, we'll expand that playbook to:

3. Prompt a user to confirm or denounce the login activity via Slack message buttons
4. Request more details on the activity via a Slack interactive dialog
5. Notify the user of the actions that will be taken based on their response

The workflow for the playbook we'll create in this tutorial is shown below

[diagram coming soon]

Let's start by [deploying Socless Slack](deploy-socless-slack.md), which contains the integrations we'll use in this tutorial
