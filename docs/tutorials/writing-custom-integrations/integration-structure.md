# Integration Structure Overview

An Integration is simply a Python function that uses the [socless_python](https://github.com/twilio-labs/socless_python) library to manage its execution lifecycle. The primary module from `socless_python` that Integrations use is the `socless_bootstrap` module. To simplify a bit, `socless_bootstrap`'s primary job is to ensure that Integrations correctly process the parameters passed to them by Playbooks, and persist and return results back to the Playbook.

Integrations are deployed to and executed by the [AWS Lambda](https://aws.amazon.com/lambda/)

The basic structure for any SOCless Integration is shown below

```python
from socless import socless_bootstrap

def handle_state(*args, **kwargs):
	"""Core action logic goes here"""
	# Implement core actions (e.g api requests) and return dictionary with desired results
	return {…}

def lambda_handler(event, lambda_context):
	return socless_bootstrap(event, lambda_context, handle_state)
```


The `handle_state` function is where the logic that defines the behavior of your integration is implemented. **It is expected to return a Python Dictionary as its output**


!!! tip
    You can and are encouraged to define as many helper functions as needed to make your `handle_state` function and integration more readable and testable. You're not required to fit all your code in `handle_state`. See our [Writing Good Integrations](../../reference/writing-good-integrations.md) Guide for more information



The `lambda_handler` serves as SOCless' entry point (i.e the first function SOCless executes when it triggers your integration), and is where the `handle_state` function is  passed to `socless_bootstrap` to handle its execution and lifecycle. **It should almost always be defined exactly as shown above.**

The `socless_bootstrap` function takes the below parameters:

| Parameter      | Description                                                                                                                                                                                                                                                                                                                                  | Required? | Default |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|---------|
| event          | Contains the `Parameters` passed to the Integration by a Playbook, as well as any additional metadata the integration may need                                                                                               | Yes       | N/A     |
| handle_state   | A function that implements our actual Integration logic. Must return a dictionary                                                                                                                                                                                                                                                       | Yes       | N/A     |
| lambda_context | The [Lambda Context object](https://docs.aws.amazon.com/lambda/latest/dg/python-context.html) passed in by AWS whenever it triggers a Lambda function. Note that this is **NOT** the same as SOCless' Playbook Execution Context Object. `socless_bootstrap` needs it internally, but as integration developers, we rarely interact with it directly                                                                                                                                                                                                                                                            | Yes       | N/A     |

Let's put this knowledge to use by writing our first integration.
