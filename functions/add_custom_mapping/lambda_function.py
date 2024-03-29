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
import boto3, os


def handle_state(key: str, value: Any):
    """
    Add a key-value pair to the Socless custom mapping table
    """
    custom_mappings_table = boto3.resource("dynamodb").Table(
        os.environ.get("SOCLESS_CUSTOM_MAPPINGS_TABLE")
    )
    response = custom_mappings_table.put_item(Item={"key": key, "value": value})
    return response


def lambda_handler(event, context):
    return socless_bootstrap(event, context, handle_state)
