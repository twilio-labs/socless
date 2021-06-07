# Deploying Our Endpoint

## Configuring our Endpoint for Deployment

Open the `serverless.yml` file. At the very bottom, add a new section named `functions` and update it as shown below
```yaml
functions:
  TutorialEndpoint:
    name: socless_[yourname]_tutorial_endpoint
    handler: lambda_function.lambda_handler
    description: Receives alerts from our tutorial detection system
    environment:
      AUTH_TOKEN: ${{ssm:/socless/[yourname]/tutorial_endpoint_token~true}}
    package:
      include:
        - functions/tutorial_endpoint
    events:
      - http:
          path: /[yourname]-tutorial
          method: post
```

--8<-- "docs-snippets/replace_yourname.md"

!!! warning "Be careful with indentation!"
    Ensure that `functions` is NOT indented under the `custom` section. Otherwise your `functions` won't get deployed but you also won't get an error about this because `serverless.yml` would think you're simply defining custom information.

In short, this snippet is a deployment configuration for a function that:

- has the **name** `socless_[yourname]_tutorial_endpoint`
- has its `handler`, i.e its first executed function, set to `lambda_function.lambda_handler`
- has a human readable `description`
- has an **environment** variable named `AUTH_TOKEN` that fetches its value from `/socless/[yourname]/tutorial_endpoint_token` path in SOCless' secret store (`ssm`) using a [Serverless Variable](../../reference/variables.md#serverless-variables).
- gets its code **package** from the `functions/tutorial_endpoint` folder
- And exposes an **http** endpoint url at **path** `/[yourname]-tutorial` that expects `POST` **method** requests


And with that, our Endpoint is now configured for deployment!

## Deploying our Endpoint

To deploy our Endpoint, execute
```
socless stack deploy
```

Once our endpoint succeeds, We should have output similar to the below

```yaml hl_lines="9-10"
Service Information
service: socless-[yourname]-tutorial-playbook
stage: sandbox
region: us-west-1
stack: socless-[yourname]-tutorial-playbook-sandbox
resources: 10
api keys:
  None
endpoints:
  POST - https://xxxxxxxxxx.execute-api.us-west-1.amazonaws.com/sandbox/[yourname]-tutorial
functions:
  TutorialEndpoint: socless_[yourname]_tutorial_endpoint
layers:
  None

Stack Outputs
[yourname]InvestigateLogin: arn:aws:states:us-west-1:xxxxxxxxxxxx:stateMachine:[yourname]InvestigateLogin
ServiceEndpoint: https://xxxxxxxxxxxx.execute-api.us-west-1.amazonaws.com/sandbox
ServerlessDeploymentBucketName: socless-[yourname]-tutorial-p-serverlessdeploymentbuck-xxxxxxxxxxxx

Serverless: [socless_integration_packager] Cleaning build directory...
Serverless: [socless_integration_packager] Removing Docker container...
Serverless: Removing old service artifacts from S3...
```

The `endpoints` section shows our Endpoints URL. Let's jot it down somewhere since we'll need it to test our endpoint next.
