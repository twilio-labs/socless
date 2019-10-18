# Introduction
Socless Playbooks are simply JSON objects that describe the actions to take and resources to use to automate a response plan.
On deployment, the JSON objects are converted to State Machines that can be executed by the [AWS Step Functions](https://docs.aws.amazon.com/step-functions/latest/dg/welcome.html) service. As such, the JSON objects are written according to the AWS States Language specification [but with some slight differences](socless-vs-stock-stepfunctions.md)

The basic, bare-bones structure for any Socless Playbook JSON object is shown below:

```
{
    "Playbook": "",
    "Comment": "",
    "StartAt": "",
    "States": {

    }
}
```

It consists of the following top-level fields:
- Playbook: (required) UpperCamelCase name of the playbook. eg. InvestigateLogin
- Comment: (optional) Human readable description of the playbook
- StartAt: (required) The starting state of the playbook
- States: (required) A description of all the states in the playbook and their relationships to each other i.e. transitions. Currently, states should be named using the Upper_Case notation e.g Send_Slack_Message


In this tutorial, we'll be implementing the `InvestigateLogin` playbook we discussed in the overview for this tutorial. Our Playbook will be triggered by the alert below

```
{
 "alert_name": "Anomalous Login IP Detected",
 "details": [{"username": "bruce.wayne", "ip": "113.63.125.3"}],
 "response_plan": "InvestigateLogin"
}
```
It will respond by taking the following steps:
- Geolocate the `ip` using our GeoIP integration
- Use our SendMessage integration to post a notifiction of the login activity + geo ip information to our #bat-signals channel

Let's start the tutorial by setting up our playbooks development environment

# Setting Up
## Clone Playbooks Template
To begin, clone and set up the `socless-playbooks-template` into your high-level project directory by running the commands below
```
git clone git@github.com:twilio/socless-playbooks-template.git socless-playbooks
cd socless-playbooks
./setup
```
The resulting `socless-playbooks` directory is a Serverless framework application that will serve as the deployment stack for ALL your Socless Playbooks going forward.

Within the `socless-playbooks` directory, create a folder named `playbooks`. This folder is where all your Playbooks will be written.

## Reference Integration ARNs in our Playbook stack
To complete the setup for our Playbooks stack, let's create references to the ARNs of the Lambda Integrations we deployed in the last tutorial so we can use those Integrations in the playbook we'll create.

Open the serverless.yml file. The `custom` section currently looks like this
```
custom:
  statesRole: ${{cf:socless-${{self:provider.stage}}.StatesExecutionRoleArn}}
  socless:
    CreateEvents: ${{cf:socless-${{self:provider.stage}}.CreateEvents}}
    MergeParallelOutput: ${{cf:socless-${{self:provider.stage}}.MergeParallelOutput}}
    Counter: ${{cf:socless-${{self:provider.stage}}.Counter}}
    AwaitMessageResponseActivity: ${{cf:socless-${{self:provider.stage}}.AwaitMessageResponseActivity}}
    SetInvestigationStatus: ${{cf:socless-${{self:provider.stage}}.SetInvestigationStatus}}
    QueryCustomMapping: ${{cf:socless-${{self:provider.stage}}.QueryCustomMapping}}
    AddCustomMapping: ${{cf:socless-${{self:provider.stage}}.AddCustomMapping}}
    CacheResults: ${{cf:socless-${{self:provider.stage}}.CacheResults}}
```
Underneath the `socless` key are references to the ARNs of the Lambda Integrations that Socless' core infrastructure ships with by default. These references will allow us use the ARNs of these Lambda integrations in our Socless playbooks.

Whenever you need to use an integration in a Socless playbook, you'll need to ensure that the ARN of the Lambda Integration is referenced here. The current convention for referencing Lambda ARNs in your playbook stack is to nest the Integration names under their relevant "product" stack in the `custom` section of the serverless.yml file. That is

```
custom:
    product:
        Integration: ${{cf:socless-product-${{self:provider.stage}}.Integration}}
```

For our tutorial, we have two integrations (GeoIP & SendMessage) that are currently deployed in our tutorial "product" stack. Reference their ARNs in our Playbook stack by adding the below code one-indentation level under our `custom` field (i.e. on the same level as the `socless` field):

```
tutorial:
    GeoIP: ${{cf:socless-tutorial-${{self:provider.stage}}.GeoIP}}
    SendMessage: ${{cf:socless-tutorial-${{self:provider.stage}}.SendMessage}}
```

We will now be able to reference the `GeoIP` and `SendMessage` Integrations in our Playbook using the variables `${{self:custom.tutorial.GeoIP}}` and `${{self:custom.tutorial.SendMessage}}` respectively.

The references rely on [The Serverless Frameworks' Variable System](https://serverless.com/framework/docs/providers/aws/guide/variables/). Be sure to review that documentation to understand how it works.

# Coding The Playbook
## Laying out Basic Structure
Our tutorial playbook will be called `InvestigateLogin`. In our `playbooks` directory, create a folder called `investigate_login`. In the `investigate_login` folder, create a file named `playbook.json`. This file is where our playbook's implementation will live. It must be called `playbook.json`.

Open the playbook.json file in your favorite text editor and layout the basic structure of our playbook as shown below:

```
{
    "Playbook": "InvestigateLogin",
    "Comment": "Playbook to investigate a login",
    "StartAt": "Geolocate_IP",
    "States": {

    }
}
```
This defines a playbook called `InvestigateLogin` that starts at a state called `Geolocate_IP`. Let's configure that `Geolocate_IP` state in the `States` object.

## Configuring the Geolocate_IP state
Our `Geolocate_IP` state will be a Task state that makes use of our GeoIP integration. Courtesy of AWS Step Functions, Socless playbooks support multiple types of states that all serve different purposes in automating a workflow. Task states are primarily used to execute actions in a playbook. Start the definition for our Geolocate_IP state by updating your playbook.json to match the code shown below
```
{
    "Playbook": "InvestigateLogin",
    "Comment": "Playbook to investigate a login",
    "StartAt": "Geolocate_IP",
    "States": {
        "Geolocate_IP": {

        }

    }
}
```
The update starts the definition for our `Geolocate_IP` state. Note that the current convention for naming states in Socless is to use `Upper_Case_Underscore_Separated` notation.

A bare-bones configuration for a Task state requires the below field:
- `Type`: The state type. For Task states, this must be set to `Task`
- `Resource`: The URI for the resource the state uses to execute its action. For Lambda Integrations, this is the ARN of the Lambda function for the Integration. Since we'll be using the GeoIP Integration, we'll specify its ARN using the `${{self:custom.tutorial.GeoIP}}` variable we configured in our serverless.yml file.
- `Parameters`: An object with a key-value mapping of all the parameters an Integration needs to complete its action. As explained in the [Parameter References & Template Variables](./Parameter-References-&-Template-Variables) documentation, there are many ways to pass parameters to Integrations depending on where the information lives. The IP address we want to geolocate in our playbook is contained in the event payload sent to our Playbook and can be referenced using the parameter `$.artifacts.event.details.ip`. Since our GeoIP integration requires an `ip`, we'll pass it the IP using the configuration `{"ip": "$.artifacts.event.details.ip"}`
- A transition configuration, either `Next` if we're transitioning to another state, or `End` if the state being configured is the final state of the playbook. Our GeoIP state will transition to "Notify_Bat_Signals_Channel" once it completes its execution, so we'll configure a `Next` transition

The full configuration of our Geolocate_IP state is shown below.
```
{
    "Playbook": "InvestigateLogin",
    "Comment": "Playbook to investigate a login",
    "StartAt": "Geolocate_IP",
    "States": {
        "Geolocate_IP": {
            "Type": "Task",
            "Resource": "${{self:custom.tutorial.GeoIP}}",
            "Parameters": {
                "ip": "$.artifacts.event.details.ip",
            },
            "Next": "Notify_Bat_Signals_Channel"
        }
    }
}
```

The GeoIP Integration used by this state returns `country`, `latitude` and `longitude`. These values will be accessible by subsequent integrations using either Parameter references in the format `$.results.Geolocate_IP.*` or Template variables in the format `{context.results.Geolocate_IP.*}` .

## Configuring the `Notify_Bat_Signals_Channel` state
Next, let's configure our `Notify_Bat_Signals_Channel` state. This state will also be a Task state. It'll use our SendMessage integration to send a message to our #bat-signals Slack channel. The message will read "`{username}` just logged in from `{latitude}, {longitude}`". Finally, our state will serve as the `End` state for our playbook.

Extend your playbook.json with the configuration for our state as shown below
```
{
    "Playbook": "InvestigateLogin",
    "Comment": "Playbook to investigate a login",
    "StartAt": "Geolocate_IP",
    "States": {
        "Geolocate_IP": {
            "Type": "Task",
            "Resource": "${{self:custom.tutorial.GeoIP}}",
            "Parameters": {
                "ip": "$.artifacts.event.details.ip"
            },
            "Next": "Notify_Bat_Signals_Channel"
        },
        "Notify_Bat_Signals_Channel": {
            "Type": "Task",
            "Resource": "${{self:custom.tutorial.SendMessage}}",
            "Parameters": {
                "target": "bat-signals",
                "target_type": "channel",
                "message_template": "`{context.artifacts.event.details.username}` logged in from `{context.results.Geolocate_IP.country_name}` at coordinates `{context.results.Geolocate_IP.latitude}`, `{context.results.Geolocate_IP.longitude}`"
            },
            "End": true
        }
    }
}
```

Voila! our InvestigateLogin playbook is completely written and ready to deploy.

# Configuring our Playbook for Deployment
Open your serverless.yml file. Add a `playbooks` sub-section underneath the `custom` section and list the folder name of the playbook as shown below
```
playbooks:
    - investigate_login
```

Our playbook is no configured for deployment.
# Deploying the Playbook
To deploy the playbook to our dev environment, execute the below command:
```
npm run dev
```
# Conclusion
Head to the AWS Step Functions Console in the AWS Region of your Socless dev environment. You should see the InvestigateLogin Playbook listed there. The easiest way to test our playbook is to send an alert to our Playbook through an Event Endpoint. So let's [create your first event endpoint](/your-first-endpoint)
