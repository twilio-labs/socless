from socless import create_events


def lambda_handler(event, context):
    try:
        # Populate event_details object with approriate fields
        event_details = {
            "event_type": "...",  # event name
            "playbook": "...",  # Playbook to Execute
            "details": [
                {...},  # alert finding
                {...},  # alert finding
            ],
        }
        # Register event and start playbook
        create_events(event_details, context)
    except Exception as e:
        return {"statusCode": 400, "body": f"{e}"}
    return {"statusCode": 200}
