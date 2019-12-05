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
from socless.utils import gen_id
from datetime import datetime
import boto3
import botocore
import json
import os


def save_to_s3(file_name, log_object, bucket_name):
    status = ''
    s3 = boto3.resource('s3')
    try:
        s3.Bucket(bucket_name).put_object(Key=file_name,Body=json.dumps(log_object))
        status = 'Success'
    except botocore.exceptions.ClientError as e:
        raise Exception("Failed to store the log file to S3:\n", e)
        status = 'Fail'
    return { "status" : status }


def lambda_handler(event,context):

    # Nest handle_state inside lambda_handler to access raw context object
    def handle_state(event_context, findings):
        """
        Create a log file and upload it to SOCless logging bucket.

        Args:
            findings (obj): The findings to be logged, and it can be any variable type that's JSON serializable

        Env:
            SOCLESS_Logs (str): The name of the bucket where you want to upload logs to

        Returns:
            A dict containing the file_id (S3 Object path) and vault_id (Socless logging bucket
            reference) of the saved content
        """
        bucket_name = os.environ.get("SOCLESS_Logs")
        log_type = "findings"
        log_source = context.invoked_function_arn
        aws_region = log_source.split(":")[3]
        aws_account = log_source.split(":")[4]
        event_type = event_context['artifacts']['event']['event_type']
        playbook_name = event_context['artifacts']['event']['playbook']
        execution_id = event_context['execution_id']
        execution_arn = "arn:aws:states:{}:{}:execution:{}:{}".format(aws_region, aws_account, playbook_name, execution_id)
        investigation_id = event_context['artifacts']['event']['investigation_id']
        event_payload = event_context['artifacts']['event']['details']
        utc_time = datetime.utcnow()
        utc_time_iso = utc_time.isoformat() + "Z"
        year = utc_time.year
        month = utc_time.month
        day = utc_time.day
        uuid = gen_id()
        file_id = "{}/{}/{}/{}/{}/{}.json".format(log_type, year, month, day, playbook_name, uuid)
        log = {
            "log_type": log_type,
            "log_source": log_source,
            "timestamp": utc_time_iso,
            "execution_arn": execution_arn,
            "investigation_id": investigation_id,
            "event_type": event_type,
            "event_payload": event_payload,
            "findings": findings
        }

        return save_to_s3(file_id, log, bucket_name)

    return socless_bootstrap(event,context,handle_state, include_event=True)
