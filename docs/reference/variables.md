# Variables in SOCless

Effective automation typically requires referencing dynamic data (variables) in workflows.

SOCless has a number of distinct Variable systems, each serving a specific scenario.


The different Variable systems can be categorized according to:

* When the variables are resolved (Deploy time or Run time)
* Where they are supported
* What they can access

The below table provides a summary of the distinctions between the Variable systems according to their categorization.


|                                                         | **Template Variables**                              | **Choice Path Variables**                                           | **Serverless Variables**                                                                                              |
|---------------------------------------------------------|-------------------------------------------------|-----------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------|
| Resolved At?                                            | Run Time                                        | Run Time                                                        | Deploy Time                                                                                                       |
| Typically Used For?                                     | Passing Parameters to Integrations/Interactions | Performing comparisons in Choice States                         | Specifying deploy-time configurations like function environment variables, Integration/Interaction `Resource` etc |
| Supported in `serverless.yml`?                          | No                                              | No                                                              | Yes                                                                                                               |
| Supported in `Parameters` of Integrations/Interactions? | Yes                                             | No                                                              | Yes                                                                                                               |
| Supported In Choice State `Variable`?                             | No                                              | Yes                                                             | Yes                                                                                                               |
| Can access Playbook Execution Context?                  | Yes                                             | Partially (only the most recent Context result can be accessed) | No                                                                                                                |
| Can access Secrets (SSM)                                | Yes, using `{{secret('/path/to/secret')}}`      | No                                                              | Yes (using `${{ssm:/path/to/secret~true}}`                                                                        |
| Can access Stack Outputs?                               | No                                              | No                                                              | Yes                                                                                                               |


## Template Variables

Template Variables are used to pass dynamic data to Integrations/Interaction States.

**They are resolved at Integration run-time** (i.e during Integration execution) and are only supported in the `Parameters` field of Integrations

Template Variables are referenced using the `{{ }}` syntax. They have access to the Playbook Execution Context, Secrets and Integration Environment variables. See examples below of how to use Template Variable syntax to reference Playbook Execution Context, Secrets and Environment Variables

=== "Access Playbook Execution Context"
    ```
    {{ context.* }}
    ```

=== "Access Secret"
    ```
    {{ secret('/path/to/secret') }}
    ```

=== "Access Environment Variable"
    ```
    {{ env('ENVIRONMENT_VARIABLE') }}
    ```


Template Variables are powered by the [Jinja2 Template Engine](https://jinja.palletsprojects.com/en/2.11.x/). Jinja2 provides a number of useful [Filters](https://jinja.palletsprojects.com/en/2.11.x/templates/#filters) that can be used to modify the value rendered by the template variable.

**Be sure to review the Jinja2 documentation for full insight into the features it provides that may be valuable to your use-case.**


 In addition to Jinja2's built-in Filters, SOCless also provides the following custom Jinja2 filters:

 | Filter/Function | Usage                                     | Examples        |
 |-----------------|-------------------------------------------------|------------------------------------------------------------------------------------------|
 | `secret()`        | Fetch a secret from the secret store            | ```{{ secret('/foo/bar') }}```  * NOTE: The single-quotes are required                   |
 | `vault()`         | Fetch content from the SOCless Vault            | ```{{ vault( context.dynamic.file.reference ) }}```   ```{{ vault('static-file-id')}}``` |
 | `env()`           | Read an environment variable                    | ```{{ vault('FOO_BAR') }}```                                                             |
 | `fromjson`        | Convert stringified JSON to a Python dictionary | ```{{ context.stringified_json | fromjson }}```                                         |


## Serverless Variables
Serverless Variables allow you to dynamically replace configuration values in your `serverless.yml` and `playbook.json`.

**They are resolved at deploy-time** and typically used to modify Playbook/Integration behavior based on the SOCless Environment (sandbox/dev/stage/prod) the Playbook/Integration is deployed to. Examples of such modifications include:

* Ensuring appropriate `Resource` is used by Integrations depending on the deployment environment they run in
* Enabling/modifying Playbook behavior based on deployment environment e.g. Ensuring scheduled events are active in prod but not dev/stage/sandbox


Serverless Variables are referenced using the syntax `${{ }}`. They are provided by the [Serverless Framework](https://www.serverless.com/framework/docs/providers/aws/guide/variables/).

Below is a quick summary of what's possible with Serverless Variable. **But be Sure to refer to the Serverless Framework documentation on Variables to explore what's possible**

!!! note
    The Serverless Variables Documentation shows the variable syntax as `${ }`. However, SOCless uses `${{ }}`

* `${{cf:name-of-cloudformation-stack.OutputName}}` - Reference output from a Cloudformation stack (e.g the ARN of a deployed integration)
* `${{ssm:/path/to/secret~true}}` - Reference and decrypt a secret from the Secret Store (SSM). The `~true` means decrypt the secret after referencing
* `${{ssm:/path/to/secret}}` - Reference a secret. Leave it encrypted if encrypted.
* `${{self:foo.bar}}` - Reference a property in the `serverless.yml` file. E.g `${{self:provider.stage}}` references the SOCless deployment environment.


## Choice Variables

Choice Variables are used in Choice States in Playbooks. They follow the syntax `$.foo.bar`.

**Currently, they only have access to parts of the Playbook Context Object that were generated by the prior executing state.**

Choice Path Variables are powered by [AWS Step Functions Path Syntax](https://docs.aws.amazon.com/step-functions/latest/dg/amazon-states-language-paths.html)
