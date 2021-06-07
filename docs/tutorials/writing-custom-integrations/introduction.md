# Developing Custom Integrations
Welcome to our tutorial on Developing Custom Integrations!

This tutorial builds on the content from the [Getting Started Tutorial](../quick-start/introduction.md) and requires that you have the completed code from that tutorial handy.

In the Getting Started Tutorial, we used SOCless' built-in [HTTPRequest Integration](../../reference/builtin-integrations/http_request.md) to integrate with our Geolocation and Slack Send Message APIs.

While the HTTPRequest Integration makes it possible to integrate with many APIs without writing code, you may sometimes have the need to implement custom functionality not supported by the HTTPRequest Integration. Examples of such functionality include:

* **Interacting with paginated APIs:** The HTTPRequest Integration does NOT support pagination. So when interacting with APIs that return paginated responses, the HTTPRequest Integration should not be used.
* **Data Manipulation/Transformations:** HTTPRequest returns data as-is from the API it integrates with. And while [Template Variables](../../reference/variables.md#template-variables) may allow for some level of data manipulation/transformation, its sometimes more robust to implement these via a custom integration
* **Handling Complex Authentication Schemes:** Some APIs have authentication schemes that aren't easy to handle in HTTPRequest (e.g. AWS APIs). In such cases, a custom Integration is right for the job

In this tutorial, we'll create two Integrations: a `GeoIP` Integration and a `SendMessage` Integration. We'll then use these Integrations in place of the HTTPRequest Integration to implement the `Geolocate_IP` and `Send_Notification_To_Slack` States in our `InvestigateLogin` Playbook.


Let's get started!

!!! tip "Integrating with AWS? We've got you covered!"
		As mentioned above, the HTTPRequest Integration is not ideal for integrating with AWS APIs. That's why SOCless also ships with a builtin [AWSRequest Integration](../../reference/builtin-integrations/aws_request.md) that's based on [AWS' Boto3 sdk](https://aws.amazon.com/sdk-for-python/)

		The AWSRequest API has full support for all AWS API endpoints (including the paginated ones :wink:)
