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
import boto3, os
from socless import *
from botocore.exceptions import ClientError


EVENTS_TABLE = os.environ.get('SOCLESS_EVENTS_TABLE')

def handle_state(investigation_id,status):
    """
    Set the Investigation ID to status.
    This is applied to the original incident
    """
    VALID_STATUSES = ['open','closed','active','whitelisted']
    if not investigation_id:
        return {"result": "failure", "message": "No investigation_id provided"}
    if status not in VALID_STATUSES:
        return {"result": "failure", "message": "Status {} is not a valid status".format(status)}

    event_table = boto3.resource('dynamodb').Table(EVENTS_TABLE)
    # Investigation_id in Socless now matches the ID of the original event ''
    try:
        update_query = event_table.update_item(
            Key={'id':investigation_id},
            UpdateExpression='SET status_ = :status_',
            ExpressionAttributeValues={':status_': status},
            ConditionExpression='attribute_exists(id)'
        )
    except ClientError as e:
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            return { "result": "failure", "message": "Investigation with id {} does not exist".format(investigation_id) }
        else:
            raise
    else:
        return {"result": "success"}

def lambda_handler(event,context):
    return socless_bootstrap(event,context,handle_state)
