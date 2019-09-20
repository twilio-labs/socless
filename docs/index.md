# SOCless

SOCless is a serverless framework built to help security teams easily automate their incident response and operations processes.

## Overview
SOCless uses the [AWS Step Functions](https://aws.amazon.com/step-functions/) and [AWS Lambda](https://aws.amazon.com/lambda/) services to execute user-defined workflows. The workflows, called Playbooks, are defined as JSON objects and triggered by real-time alerts from data sources or [AWS CloudWatch](https://aws.amazon.com/cloudwatch) schedules.

[![SOCless Base Architecture](imgs/socless-base-architecture.png)](imgs/socless-base-architecture.png)
(Click to enlarge)

## Features
- Responds to real-time or scheduled events
- Orchestrates existing security tools into workflows using AWS Lambda functions written in Python 3
- Interact with humans as part of automated workflows and adapt to their responses
- Static IP address that can be whitelisted to internal resources
- Rapid automation development life-cycle courtesy of reusable, modular and shareable plugins
- Infrastructure and response workflows deploy as code using [The Serverless Framework](https://serverless.com)
- Serverless design has low cost, low operational overhead, and scales effortlessly


To get started, [deploy SOCless!](/deploying-socless)
