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
from socless import (
    setup_socless_global_state_from_running_step_functions_execution,
    SoclessEventsError,
)


def lambda_handler(event, _):
    try:
        execution_id = event["execution_id"]
        playbook_name = event["playbook_name"]
        playbook_event_details = event["playbook_event_details"]
    except KeyError as e:
        raise SoclessEventsError(
            f"Missing parameter to convert directly invoked step functions execution to a SOCless Playbook {e}"
        )

    try:
        reformatted_playbook_input = (
            setup_socless_global_state_from_running_step_functions_execution(
                execution_id, playbook_name, playbook_event_details
            )
        )
    except Exception as e:
        raise SoclessEventsError(
            f"Unable to use SF execution input to setup socless. Error: {e}"
        )
    return reformatted_playbook_input
