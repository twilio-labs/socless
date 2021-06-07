# Playbooks Reference Documentation

## Scheduling Playbook Execution

SOCless Playbooks can be configured to execute on a schedule. This is done in the serverless.yml as shown below

```yaml hl_lines="4-9"
custom:
  playbooks:
    - example_scheduled_playbook:
        events:
          - schedule:
              rate: "cron(0 12 * * ? *)"
              description: "Sample playbook schedule"
              enabled: true
              input: '{"json": "payload"}'
```

The fields are as follows

- `rate`: Schedule's rate of execution. This most be one of `cron()` or `rate()` types as described in the [Schedule Expressions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html#CronExpressions) documentation. See listed documentation for details
- `description`: Human readable description of the schedule
- `enabled`: Set to `true` to enable a schedule or `false` to disable it
- `input`: **A valid JSON string** representing the input to pass to the playbook when the schedule executes


If your SOCless Playbook is deployed in multiple environments, you might want your schedule enabled in some environments but not others. This can be accomplished as shown below

```yaml hl_lines="2-6 13"
custom:
  scheduleEnabled:
    sandbox: false
    dev: false
    stage: false
    prod: true
  playbooks:
    - example_scheduled_playbook:
        events:
          - schedule:
              rate: "cron(0 12 * * ? *)"
              description: "Sample playbook schedule"
              enabled: ${{self:custom.scheduleEnabled.${{self:provider.stage}}}}
              input: '{"json": "payload"}'
```

The above shows an example of how you might configure a schedule that is `enabled` in `prod` but not in `dev`, `stage`, or `sandbox`
