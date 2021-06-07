# Operational Monitoring

## Playbook Execution Logs

SOCless Playbook Execution logs are AWS Step Functions Logs. To enable them,

* Ensure your SOCless Playbook stacks are using an sls-apb version that's >= 1.2.0
* Ensure you're using a SOCless core infrastructure version >1.0.0
* Set `custom.sls_apb.logging` to `true` in the `serverless.yml` for your Playbook stacks.

Once enabled, All Playbook Execution logs will be generated and centralized in a Cloudwatch Log group called `/socless/playbook-execution-logs`. They will also be stored in the SOCless Logs bucket at the bucket path `/playbook_executions`

If you have a log aggregation Platform, we suggest you ingest these logs into the platform for monitoring. The full list of events the log contain can be found on [this AWS Documentation Page](https://docs.aws.amazon.com/step-functions/latest/dg/cloudwatch-log-level.html).

SOCless collects at Log level `ALL` but does not include the execution data (i.e input and output for each state) in the logs as these could contain sensitive information.
