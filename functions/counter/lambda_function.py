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
from socless import socless_bootstrap
import operator


def handle_state(context, state_name, start, delta, direction="up"):
    """
    Simple Counter
    Context: Socless Input object
    state_name: Name of the Socless state
    start: Starting value of the counter
    delta: Amount to change counter by
    direction: Direction of the change
    """
    DIRECTIONS_MAP = {"up": operator.add, "down": operator.sub}
    if direction not in DIRECTIONS_MAP:
        return {
            "status": "Error",
            "message": "Unsupported direction supplied to counter",
        }
    start = int(start)
    delta = int(delta)
    updated_count = {}
    current_count = context.get("results", {}).get(state_name, {})
    if current_count:
        current_value = current_count["current_value"]
        updated_count["previous_value"] = current_value
        updated_count["current_value"] = DIRECTIONS_MAP[direction](current_value, delta)
    else:
        updated_count["previous_value"] = start
        updated_count["current_value"] = DIRECTIONS_MAP[direction](start, delta)
    return updated_count


def lambda_handler(event, context):
    return socless_bootstrap(event, context, handle_state, include_event=True)
