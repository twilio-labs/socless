# Key Concepts and Terms
Below are key concepts and terms to help you get started with SOCless:

- **Playbooks**: The automated processes you create. Playbooks contain a series of coordinated steps that work towards an end goal. They are written in JSON
- **[AWS Step Functions](https://aws.amazon.com/step-functions)**: The AWS service that manages playbook executions.
- **State**: A single step in a playbook. States can take actions, evaluate choices, parallelize actions, wait for time periods, or aid debugging of playbooks.
- **Integrations**: AWS Lambda functions that integrate with your existing security products. States use integrations to take actions in playbooks. Integrations are written in Python. The term may refer to a single function, or a group of functions related to the same product.
- **Event Endpoints**: AWS Lambda functions that process incoming events and trigger playbook executions.
- **Event Triggers**: Services that trigger event endpoints. Currently tested event triggers include AWS API Gateway for http-based alerts, and AWS CloudWatch for scheduled events. However, any service that can trigger an AWS Lambda function may serve as an event trigger.
- **Event Table**: The AWS DynamoDB table that stores event data. Event endpoints create events in the Event Table.
- **Execution Results Table**. The AWS DynamoDB table that stores playbook execution data. Integrations read input and write outputs to the Execution Results Table as they perform actions during a playbook's execution.
- **socless_python**: The Python library that manages the execution life-cycle of integrations and event endpoints, making them simple to write, reuse and share.
