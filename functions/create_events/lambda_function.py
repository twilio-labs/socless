# Copyright 2018 Twilio, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License
from typing import List
from socless import socless_bootstrap, create_events


def lambda_handler(event, context):

    # Disclaimer: having the handle_state in the lambda_handler is a quick & dirty solution to the problem of exposing the lambda 'context' object to the handle_state function
    # so that the `create_events` function can use it. There should probably be a better way to do so.
    def handle_state(
        event_context,
        event_type: str,
        details: List[dict],
        playbook="",
        dedup_keys: list = [],
        data_types: dict = {},
        add_to_details: dict = {},
    ):
        """
        Creates a new event in Socless using the socless_create_events api from the socless_python library

        Args:
            event_type (str): Human Readable Event name e.g 'Investigate Login'
            details (list): List of dictionaries containing the event details
            playbook (str): The name of the playbook to execute
            dedup_keys (list): The keys to use to deduplicate the event
            data_types (dict): A mapping of what datatypes are contained in the event details
            add_to_details (dict): A dictionary containing additional keys to add to each details dict
        Returns:
            A dict containing a boolean status code and, if successful, the investigation id assigned to the created event.
        """

        execution_id = event_context.get("execution_id", "n/a")

        for each in details:
            each.update(add_to_details)

        events = {
            "event_type": event_type,
            "details": details,
            "data_types": data_types,
            "playbook": playbook,
            "dedup_keys": dedup_keys,
            "event_meta": {
                "data source": f"Execution: {execution_id}",
                "description": "Event created from within a Playbook",
            },
        }

        create_events(events, context)
        return {"completed": True}

    return socless_bootstrap(event, context, handle_state, include_event=True)
