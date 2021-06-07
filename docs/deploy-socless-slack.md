## Deploy Socless Slack Integrations
Socless Slack is a set of integrations and endpoints for enabling human interactions via Slack.

Socless Slack includes functionality for:

* Prompting a user to answer yes-no questions for interactive buttons
* Requesting detailed information using dialogs
* Collecting information via Slack slash command entry

Follow the instructions in the [socless-slack README](https://github.com/twilio-labs/socless-slack) to deploy and configure credentials for Socless Slack.

## Reference Socless Slack Integrations in Socless Playbook Repository
Next, let's update the serverless.yml file of our socless-playbooks repository with references to the integrations provided by Socless Slack. If you no longer have the socless-playbooks repository we created in the Getting Started tutorial, you can download it from the [Socless Examples repo](https://github.com/twilio-labs/socless-examples/tree/master/getting-started-tutorial)

Open up the serverless.yml file for your socless-playbooks repo and nest the below configurations one indentation level below the `custom` object

```
slack:
    PromptForConfirmation: ${{cf:socless-slack-${{self:provider.stage}}.PromptForConfirmation}}
    PromptForResponse: ${{cf:socless-slack-${{self:provider.stage}}.PromptForResponse}}
    SendMessage: ${{cf:socless-slack-${{self:provider.stage}}.SendMessage}}
    FindUser: ${{cf:socless-slack-${{self:provider.stage}}.FindUser}}
    SendDialog: ${{cf:socless-slack-${{self:provider.stage}}.SendDialog}}
```
The configuration references the five Lambda integrations currently made available by Socless Slack. We'll use them shortly



Once the configuration is saved, head to the next page for an overview of SOCless' Human Interaction Workflow
