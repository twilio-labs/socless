# Tutorial Series Introduction

Welcome to the SOCless Tutorial series!

Here's an overview of what we'll cover in the series

* [Getting Started](../tutorials/quick-start/introduction.md) covers the basics of writing playbooks and using SOCless' builtin HTTPRequest Integration
* [Developing Custom Integrations](../tutorials/writing-custom-integrations/introduction.md) teaches you how to write integrations.
* [Human Interaction Tutorial](../tutorials/human-interaction/interacting-via-slack.md) covers how to add Slack-based manual approval steps to your workflows


We recommend you take these tutorials in order as they build on each other and cover unique concepts.

Throughout the course of our tutorials we will assume you have basic familiarity with

* Executing shell commands in a terminal
* Working in code editors like [Visual Studio Code](https://code.visualstudio.com/) or [Atom](https://atom.io/)
* Writing JSON and YAML files

In addition, we'll assume that you have:

* a MacOS laptop or other *nix-style operating system.
* an existing SOCless `sandbox` environment deployed
* the `socless_cli` installed on your local machine and configured for access to that SOCless sandbox environment
* A Slack instance and a Slack Bot Token saved to the path `/socless/slack/bot_token` in SOCless Secret Store (i.e AWS SSM Parameter Store).
* (optional) A Twilio account & Twilio Phone Number with SMS Capabilities

!!! note
    - If your SOCless instance has an administrator, work with them to get setup for this tutorial
    - If you are the SOCless administrator, refer to our [Deploying SOCless](../deploying-socless.md) & [Setting Up A Slack Bot](../reference/setting-up-a-slack-bot.md) reference guides for instructions on setting up


We will **NOT** assume familiarity with the following

* AWS services SOCless uses
* Serverless Framework

Over the course of the tutorials we will provide information about them as needed to aid the learning experience.

Below are some tips and notes to keep in mind as you work through the tutorials

!!! tip "Tip: Write the code!"
    Our tutorials feature a lot of code snippets. While you can simply copy-paste them, we strongly recommend typing them out by hand (unless explicitly asked to copy-paste it). This will help you develop a stronger understanding of the material.



!!! note "Note: Replace [yourname]!"
    You'll occasionally find the snippet `[yourname]` in code samples. If you're taking the SOCless tutorial in a shared sandbox environment, we expect you to replace that snippet with your actual name.

    For example, if your name is Alfred, when you find a string like `socless_[yourname]_endpoint` in the tutorial, you're expected to replace it with `socless_alfred_endpoint`. This will help prevent your code colliding with other peoples' code in your sandbox when you deploy.


!!! tip "Tip: Stay organized!"
    As you work through all our tutorial series, you'll create a number of SOCless repositories.

    To help you stay organized, we encourage you to keep all your SOCless repos in a single folder.

    The name of the folder doesn't matter but if you're unsure what to call, it you can name it `Projects`. For the remainder of this tutorial, we'll assume you have a `Projects` folder in your home directory


Use the `Next` button at the bottom of this page to get started! Enjoy!
