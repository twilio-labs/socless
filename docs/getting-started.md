This tutorial will take you through the basics of creating your first automated response plan in Socless.

In Socless, automated response plans are called playbooks. Our first playbook will respond to an alert of an anomalous login. The alert will contain the username of the account that was logged into and the IP that logged into it. Our playbook, which will be called "InvestigateLogin", will respond to the alert by geolocating the IP address and posting the findings to a Slack channel.

To accomplish this, we will:

* Create one Socless Integration that handles IP geolocation and another that can send a slack message
* Create a playbook that uses the above Integrations to respond for our alert
* Create a Socless Endpoint that knows how to process our alert and trigger our playbook

Here's a diagram that shows how all the components we will create fit together to respond to our alert

[ diagram coming soon ]

Head to the next page to create your first integration
