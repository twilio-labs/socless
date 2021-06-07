# Deploying Our Playbook
## Configuring Our Playbook for Deployment

SOCless infrastructure is deployed using the [Serverless Framework](https://serverless.com/). As such, all SOCless Stacks have a `serverless.yml` which is used to configure Playbooks, Integrations, Endpoints and other Resources for deployment.

To deploy our playbook:

- Open the `serverless.yml` file that exists in your `socless-tutorial-playbook` folder. There should be a section called `custom` with a subsection called `playbooks`. It should look similar to the below
```yaml hl_lines="9"
custom:
  soclessPackager:
    buildDir: build
  core:
    SetInvestigationStatus: ${{cf:socless-${{self:provider.stage}}.SetInvestigationStatus}}
    MergeParallelOutput: ${{cf:socless-${{self:provider.stage}}.MergeParallelOutput}}
    HTTPRequest: ${{cf:socless-${{self:provider.stage}}.HTTPRequest}}
    AWSRequest: ${{cf:socless-${{self:provider.stage}}.AWSRequest}}
  playbooks:
```
- List our `investigate_login` folder name under the playbooks section as such
```yaml hl_lines="11"
custom:
  soclessPackager:
    buildDir: build
  core:
    SetInvestigationStatus: ${{cf:socless-${{self:provider.stage}}.SetInvestigationStatus}}
    MergeParallelOutput: ${{cf:socless-${{self:provider.stage}}.MergeParallelOutput}}
    HTTPRequest: ${{cf:socless-${{self:provider.stage}}.HTTPRequest}}
    AWSRequest: ${{cf:socless-${{self:provider.stage}}.AWSRequest}}

  playbooks:
    - investigate_login
```

That's it! Configuring a Playbook for deployment is a simple as listing the name of the playbook folder (in the `playbooks` directory) under the `playbooks` section of our `serverless.yml`. The rest is be handled for us by SOCless when we deploy our stack

!!! tip "Remove our sample code!"
    You may have noticed another playbook called `socless_[yourname]_tutorial_playbook_integration_test` configured in the `playbooks` section. This is a sample playbook that ships with our `socless-template`.

    You can take a look at the playbook to see it what it does but afterwards, feel free to delete that line from your `serverless.yml`, as well as the folder for that playbook from your `socless-tutorial-playbooks/playbooks` folder so that we don't accidentally deploy it with our playbook.


    You should also delete the `functions`, `resources` and `Outputs` sections as well so that the `playbooks` section is the last section in our file.

## Deploying our Playbook

To deploy our Playbook, open a command line and execute the below command. Make sure you're executing it in the same directory that has our `serverless.yml` file.

```
socless stack deploy
```

!!! note
    `socless stack deploy` is really a shortcut for `socless stack deploy sandbox`, which tells the socless_cli to deploy a Stack to the SOCless sandbox environment. You can execute `socless stack deploy --help` to learn about your other options



If the command executes successfully, you should see some final output similar to the below

```yaml
Service Information
service: socless-[yourname]-tutorial-playbook
stage: sandbox
region: us-west-1
stack: socless-[yourname]-tutorial-playbook-sandbox
resources: 3
api keys:
  None
endpoints:
  None
functions:
  None
layers:
  None

Stack Outputs
[yourname]InvestigateLogin: arn:aws:states:us-west-1:xxxxxxxxxxxx:stateMachine:[yourname]InvestigateLogin
ServerlessDeploymentBucketName: socless-[yourname]-tutorial-p-serverlessdeploymentbuck-xxxxxxxxxxxx

Serverless: [socless_integration_packager] Cleaning build directory...
Serverless: [socless_integration_packager] Removing Docker container...
```

Let's go ahead and test our playbook.
