# SOCless - serverless security orchestration, automation and response

SOCless is a serverless framework built to help security teams easily automate their incident response and operations workflows.

# Overview

SOCless uses the AWS Step Functions and AWS Lambda services to execute user-defined workflows. The workflows, called Playbooks, are defined as JSON objects and triggered by real-time alerts from data sources or AWS CloudWatch schedules.

![](https://twilio-labs.github.io/socless/imgs/socless-base-architecture.png)    

Features
---
- Responds to real-time or scheduled events
- Orchestrates existing security tools into workflows using AWS Lambda functions written in Python 3
- Interact with humans as part of automated workflows and adapt to their responses
- Static IP address that can be whitelisted to internal resources
- Rapid automation development life-cycle courtesy of reusable, modular and shareable plugins
- Infrastructure and response workflows deploy as code using [The Serverless Framework](https://serverless.com)
- Serverless design has low cost, low operational overhead, and scales effortlessly

Ready? Check out the [docs!](https://twilio-labs.github.io/socless/)

Join our [community Slack workspace](https://join.slack.com/t/socless/shared_invite/enQtODA3ODEzNzcwNDgxLTBiYjVjYjI4ODI4YTY5YzM4OWRlYjQ1Yzg4M2EzMGUzMGMyYThlN2U5NTI5OWIwZWE1ZTcwNjA2MjgyZDRmMjg)


# Development Guide

## Building and Redeploying the Docs

SOCless documentation is contained in the docs folder and is powered by [MkDocs](https://www.mkdocs.org/) and [MkDocs Material](https://squidfunk.github.io/mkdocs-material/). The built docs are hosted on Github pages

**To setup your environment for building the docs**

```
python3 -m venv venv
. venv/bin/activate
pip install -r docs-requirements.txt
```

**To serve the docs locally (after setup)**
```
mkdocs serve
```

**To deploy the docs to Github pages**
```
mkdocs gh-deploy
```
