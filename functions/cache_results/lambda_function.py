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
from typing import Any
from socless import socless_bootstrap


def handle_state(execution_context, entries: Any):
    """
    This integration helps to cache, return and (optionally) re-map fields of data so that it can be used by other States. Choice states particularly benefit from this integration as
    Choice states can only refer the return results that are one step before it. This cache function can be used to pull data from earlier states not immediately preceeding the choice state so that it can be used by Choice States.
    The integration can also be used to re-map result fields from other integrations.

    Args:
        "entries": Any data you want to cache.

    Returns:
        A dictionary that contains the thing you want to be cached.
        {"cached": data}
    """
    if isinstance(entries, dict):
        new_entries = {}
        for key, value in list(entries.items()):
            if isinstance(value, str):
                new_entries[key] = value
            else:
                new_entries[key] = value
        entries = new_entries
    return {"cached": entries}


def lambda_handler(event, context):
    return socless_bootstrap(event, context, handle_state, include_event=True)
