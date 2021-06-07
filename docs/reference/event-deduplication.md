# Event Deduplication in SOCless

Key points:

* Purpose of the deduplication is to prevent erroneous duplication of effort when responding to events.
* Deduplication occurs as data is being ingested by an Endpoint.
* Responders specify deduplication keys (dedup_keys) as part of event payload. If deduplication keys are not specified in payload, deduplication does not occur.
* An event is a duplicate if it has a deduplication hash in the Dedup table that maps to an unclosed event in the Events table.
* Duplicate events are also written to the Events table and also trigger playbook executions. Duplicate events are created in `closed` status.
* Playbook authors are responsible for deciding how duplicate events are handled in their playbook executions. 
* `{{context.artifacts.events.is_duplicate}}` field can be used in playbooks to determine if an execution is operating on a duplicate event.


## Introduction 
SOCless ships with a deduplication algorithm that deduplicates events as they are ingested by an Endpoint. The aim of the algorithm is to prevent erroneous duplication of effort when responding to events.

## How SOCless Deduplicates Events
The deduplication algorithm is designed to give responders the flexibility to specify the data fields within an event body that SOCless should consider when deduplicating an event. The data fields considered when deduplicating an event are called 'deduplication keys' and are specified by including a `dedup_keys` field in the event payload (either at the source of the event such as a log aggregation platform, or in the Endpoint function). The values mapped to the deduplication keys are called the 'deduplication values' and are the actual values from the event body that are considered when deduplicating an event.



Let's use the example payload below to learn how deduplication works in SOCless. The payload shows an event body ("details") with four fields – username, location, service and count – as well as payload fields (event_type, dedup_keys, playbook, data_types) which SOCless uses to figure out how to handle the event body. Of the four fields in the event body, only "username" and "location" are specified as deduplication keys.

```json
{
	"event_type": "High-Risk Location Login",
	"playbook": "HighRiskLocationLogin",
	"details": [{
		"username": "ubalogun",
		"location": "Gotham",
		"service": "Company VPN",
		"count": 20
	}],
	"data_types": {},
	"dedup_keys": ["username", "location"]
}
```

To deduplicate an event, SOCless:

* Creates a deduplication signature by concatenating the lowercase event_type value with the sorted lowercase deduplication values. (Yielding "high-risk location logingothamubalogun" as the deduplication signature for the above payload)
* Generates a deduplication hash (dedup_hash) by running the deduplication signature through the MD5 hashing algorithm. (Yielding 7cfbdd2ab7f0534106b99d15a419e1cb for the above payload)
* Queries the Dedup Table – which contains a mapping of dedup_hashes to non-duplicate (original) events – for the computed dedup_hash and the associated event_id.
* Queries the Events Table using the event_id to retrieve the 'original' event
Creates a duplicate event if the original event is unclosed
* If SOCless runs through the deduplication algorithm for an event and does not find:
    * the dedup_hash in the Dedup Table, OR
    * an unclosed event mapped to the dedup_hash in the Event Table

    It will create the event as an original event and add the dedup_hash → event_id mapping to the Dedup Table.


If no dedup_keys are set in the event payload, SOCless will not deduplicate the event and will automatically create the event as an original event.

Why SOCless Deduplicates Events The Way It Does
<coming soon to a doco near you>
