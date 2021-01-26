# Event Deduplication

## Summary:

- The purpose of the deduplication is to prevent erroneous duplication of effort when responding to events.
- Deduplication occurs as data is being ingested by an Endpoint.
- Responders specify deduplication keys (`dedup_keys`) as part of event payload. SOCless uses these keys to deduplicate the event. If deduplication keys are not specified in payload, deduplication does not occur.
- An event is a duplicate if it has a deduplication hash in the Dedup table that maps to an unclosed event in the Events table.
- Duplicate events are also written to the Events table and also trigger playbook executions. Duplicate events are created in 'closed' status.
- Playbook authors are responsible for deciding how duplicate events are handled in their playbook executions.
`$.artifacts.events.is_duplicate` field can be used in playbooks to determine if an execution is operating on a duplicate event.

## Introduction
SOCless ships with a deduplication algorithm that deduplicates events as they are ingested by an Endpoint. The aim of the algorithm is to prevent erroneous duplication of effort when responding to events.

## How SOCless Deduplicates Events

The deduplication algorithm is designed to give responders the flexibility to specify the payload fields within an event body that SOCless should consider when deduplicating an event. The payload fields considered when deduplicating an event are called "deduplication keys" and are specified by including a `dedup_keys` field in the event payload (either at the source of the event such as a log aggregation platform, or in the Endpoint function). The values mapped to the deduplication keys are called the "deduplication values" and are the actual values from the event body that are considered when deduplicating an event.


Let's use the example payload below to learn how deduplication works in SOCless. The payload shows an event body ("details") with five fields – `username`, `location`, `service`, `count`, `login_time` – as well as payload fields (`event_type`, `dedup_keys`, `playbook`, `data_types`) which SOCless uses to figure out how to handle the event body. Of the five fields in the event body, only `username` and `location` are specified as deduplication keys.

```
{
    "event_type": "High-Risk Location Login",
    "playbook": "HighRiskLocationLogin",
    "details": [{
        "username": "ubalogun",
        "location": "Gotham",
        "service": "Company VPN",
        "count": 20,
        "login_time": "12:00 AM"
    }],
    "data_types": {},
    "dedup_keys": ["username", "location"]
}
```

To deduplicate the above event, SOCless:

- Creates a deduplication signature by concatenating the lowercase `event_type` value with the sorted lowercase deduplication values. (Yielding `high-risk location logingothamubalogun` as the deduplication signature for the above payload)
- Generates a deduplication hash (`dedup_hash`) by running the deduplication signature through the MD5 hashing algorithm. (Yielding `7cfbdd2ab7f0534106b99d15a419e1cb` for the above payload)
- Queries the Dedup Table – which contains a mapping of dedup hashes to non-duplicate (original) events – for the computed `dedup_hash` and the associated `event_id`.
- Queries the Events Table using the `event_id` to retrieve the 'original' event
- Creates a duplicate event if the original event is unclosed

If SOCless runs through the deduplication algorithm for an event and does not find:
- the `dedup_hash` in the Dedup Table, OR
- the unclosed event mapped to the `dedup_hash` in the Event Table

It will create the event as an original event and add the `dedup_hash` → `event_id` mapping to the Dedup Table.


If no `dedup_keys` are set in the event payload, SOCless will not deduplicate the event and will automatically create the event as an original event.

For further example, based on the algorithm above, the below payload would be considered a duplicate of the event above because `event_type`, `username` and `location` values are the same, despite `service`, `count` and `login_time` values being different. The prior sentence assumes that the event above is still `open` in SOCless

```
{
    "event_type": "High-Risk Location Login",
    "playbook": "HighRiskLocationLogin",
    "details": [{
        "username": "ubalogun",
        "location": "Gotham",
        "service": "GCPD Detective VPN",
        "count": 4,
        "login_time": "12:30 AM"
    }],
    "data_types": {},
    "dedup_keys": ["username", "location"]
}
```

On the other hand, the below payload would NOT be considered a duplicate of the above payloads because `event_type` is different, despite all other fields being the same

```
{
    "event_type": "Low-Risk Location Login",
    "playbook": "HighRiskLocationLogin",
    "details": [{
        "username": "ubalogun",
        "location": "Gotham",
        "service": "GCPD Detective VPN",
        "count": 4,
        "login_time": "12:30 AM"
    }],
    "data_types": {},
    "dedup_keys": ["username", "location"]
}
```

## How Duplicate Events are identified in playbooks
When SOCless deduplicates an event, it adds a field to the playbook context object called `is_duplicate`. This field is accessible in Playbooks using the path reference `$.artifacts.events.is_duplicate`. In a playbook, a playbook author can configure a Choice State that checks `$.artifacts.event.is_duplicate` to determine if the event being processed is a duplicate event.

## Why SOCless Deduplicates is Designed This Way

We observed that the definition of "duplicate event" tends to differ depending on the use-case being addressed. As such we designed the deduplication algorithm to be customizable per Event Type to enable SOCless users define for themselves what makes one event a duplicate of another.

Naturally, this means that SOCless will not make any assumptions about how an event type should be deduplicated, and by extension, will not deduplicate an event type unless deduplication has been configured by the user for that event type. We believe this is a small trade-off that buys users the freedom to deduplicate events as they wish.


## Known Issues/Features/Fixes You Can Help With
- Currently, duplicate events still trigger playbook executions. As such, if a playbook author wishes to "do nothing" for duplicate events, they need to build that logic into their playbooks by checking the value of `$.artifacts.events.is_duplicate`. While this is by design (as we want to encourage people to be explicit about how SOCless should handle duplicate events), we recognize that it might be nice to support a "do nothing" flag that instructs SOCless not to trigger playbook executions if the event is a duplicate. This flag would ideally be implemented in socless_python create_events workflow
- When a playbook executes on a duplicate event, data from the original event is not made available to the duplicate event. However, we think being able to access data from an original event while processing a duplicate event could be useful. This functionality would ideally be implemented in socless_python's parameter parsing functionality

Please feel free to start an issue on Github to address any of these concerns and to engage with us in [our Slack workspace](https://join.slack.com/t/socless/shared_invite/enQtODA3ODEzNzcwNDgxLTBiYjVjYjI4ODI4YTY5YzM4OWRlYjQ1Yzg4M2EzMGUzMGMyYThlN2U5NTI5OWIwZWE1ZTcwNjA2MjgyZDRmMjg) for details on how to contribute
