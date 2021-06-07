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
import boto3, simplejson as json, os
from socless import *

SLACK_TABLE = os.environ.get('MESSAGE_RESPONSES_TABLE')
AWAIT_SLACK_RESPONSE_ARN = os.environ['AWAIT_MESSAGE_RESPONSE_ARN']

def lambda_handler(event, context):
    # TODO implement
    stepfunctions = boto3.client('stepfunctions')
    task = stepfunctions.get_activity_task(
        activityArn=AWAIT_SLACK_RESPONSE_ARN,
        workerName='socless_outbound_message_response_workflow')

    task_token = task['taskToken']
    task_input = json.loads(task['input'])
    message_id = task_input.get('results',{}).get('message_id')
    slack_table = boto3.resource('dynamodb').Table(SLACK_TABLE)
    # Update the approriate field with the taskToken
    update_response = slack_table.update_item(
        Key={'message_id':message_id},
        UpdateExpression='SET await_token = :val1',
        ExpressionAttributeValues={ ':val1': task_token }
        )
    socless_log.info('Saved taskToken to Message Response Table', {'message_id': message_id, 'event': event})
    return update_response
