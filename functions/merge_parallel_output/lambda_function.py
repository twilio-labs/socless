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
def lambda_handler(event, context):
    if not event:
        return {}

    first = event[0]
    for output in event[1:]:
        for key,value in list(output.items()):
            if isinstance(value,dict):
                first[key].update(value)
            else:
                first[key] = value

    return first
