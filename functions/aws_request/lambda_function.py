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
import boto3
from botocore.exceptions import UnknownServiceError, OperationNotPageableError
from botocore.response import StreamingBody
from dataclasses import dataclass
from typing import Any, Callable
from datetime import datetime
from socless.exceptions import SoclessException
from socless import socless_bootstrap, vault
import json


@dataclass
class IAMToken:
    access_key_id: str
    secret_access_key: str
    session_token: str


def make_boto_response_json_serializable(response_obj: Any) -> Any:
    """
    Boto3 returns a dict by default for service responses. However,
    some of the values in the dictionary may be objects that aren't readily
    serializable by json.dumps, e.g StreamingBody, datetime.datetime, etc

    This function recursively converts those objects to strings by calling their appropriate method
    """
    # Types that should pass through this function unmodified
    PASS_THROUGH_TYPES = (str, int, float, bool, type(None))

    if isinstance(response_obj, PASS_THROUGH_TYPES):
        return response_obj
    elif isinstance(response_obj, dict):
        return {
            key: make_boto_response_json_serializable(value)
            for key, value in response_obj.items()
        }
    elif isinstance(response_obj, datetime):
        return str(response_obj)
    elif isinstance(response_obj, StreamingBody):
        return response_obj.read().decode("utf-8")
    elif isinstance(response_obj, (list, tuple)):
        return [make_boto_response_json_serializable(value) for value in response_obj]
    else:
        raise SoclessException(
            f"Attempting to serialize unsupported object type of {type(response_obj)}. The integration will need to be updated to support this type"
        )


def call_service_operation_with_pagination(
    client, operation: str, operation_parameters: dict
) -> dict:
    """Call a paginated operation and return the results"""
    try:
        paginator = client.get_paginator(operation)
        page_iterator = paginator.paginate(**operation_parameters)
        result_pages = [
            make_boto_response_json_serializable(page_response)
            for page_response in page_iterator
        ]
        return {"ResultPages": result_pages}
    except OperationNotPageableError as e:
        raise SoclessException(
            f"'{operation}' operation is not pageable. Set pagination parameter to False when calling this operation"
        ) from e
    except Exception as e:
        raise SoclessException(
            f"Failed to call paginated operation '{operation}' because {e}"
        ) from e


def call_service_operation(client, operation: str, operation_parameters: dict) -> dict:
    """Call an AWS operation without pagination using a boto3 client and return the raw unprocessed results"""

    try:
        service_operation = getattr(client, operation)
        response = service_operation(**operation_parameters)
        return make_boto_response_json_serializable(response)
    except AttributeError as e:
        raise SoclessException(
            f"'{operation}' is not a valid operation for {client.meta.service_model}"
        ) from e
    except Exception as e:
        raise SoclessException(
            f"Failed to call operation '{operation}' because {e}"
        ) from e


def determine_operation_handler(
    client, operation: str, pagination_disabled: bool
) -> Callable:
    """Determine the appropriate handler to use for the service operation"""
    if client.can_paginate(operation) and pagination_disabled is False:
        return call_service_operation_with_pagination
    else:
        return call_service_operation


def make_service_client(service_name: str, iam_token: IAMToken = None):
    """Makes the appropriate client for a service"""
    try:
        if iam_token:
            return boto3.client(
                service_name,
                aws_access_key_id=iam_token.access_key_id,
                aws_secret_access_key=iam_token.secret_access_key,
                aws_session_token=iam_token.session_token,
            )
        else:
            return boto3.client(service_name)
    except UnknownServiceError as e:
        raise SoclessException(
            f"'{service_name}' is not a supported AWS service"
        ) from e
    except Exception as e:
        raise SoclessException(
            f"Failed to make the service_client for {service_name} because {e}"
        ) from e


def assume_role(
    assume_role_config: dict, client=make_service_client("sts")
) -> IAMToken:
    """
    Assumes a role and returns the credentials for that role

    For the shape of the assume_role_config object, see
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.assume_role
    """

    DEFAULT_ASSUME_ROLE_PARAMS = {"RoleSessionName": "SOClessAWSRequestIntegration"}

    final_assume_role_params = {**DEFAULT_ASSUME_ROLE_PARAMS, **assume_role_config}

    try:
        response = client.assume_role(**final_assume_role_params)
        return IAMToken(
            access_key_id=response["Credentials"]["AccessKeyId"],
            secret_access_key=response["Credentials"]["SecretAccessKey"],
            session_token=response["Credentials"]["SessionToken"],
        )
    except Exception as e:
        raise SoclessException(f"Failed to assume role because {e}") from e


def make_aws_request(
    service_name: str,
    operation: str,
    operation_parameters: dict,
    assume_role_config: dict,
    disable_pagination: bool = False,
) -> dict:
    """Makes an AWS Request and returns the processed results"""
    iam_tokens = assume_role(assume_role_config)
    service_client = make_service_client(service_name, iam_tokens)
    call_operation = determine_operation_handler(
        service_client, operation, disable_pagination
    )
    return call_operation(service_client, operation, operation_parameters)


def handle_state(
    service_name: str,
    operation: str,
    operation_parameters: dict,
    assume_role_config: dict,
    disable_pagination: bool = False,
    save_to_vault: bool = False,
) -> dict:
    """
    The AWS Request integration enables users call any AWS API.
    It uses the AWS official SDK, boto3, to make its calls.

    At a high-level, the integration works by

     - assuming a user-configured delegate IAM role in a target-account
     - calling the specified AWS operation in the target-account
     - Returning the results

    This functinonality enables users leverage the integration for cross-account AWS automation use-cases.

    To use this integration successfully, the user-configured delegate IAM Role must have:

    - the permissions required to perform the desired operations in the target-account
    - a Trust-policy that allows the `SOCless Lambda Execution role` to assume it.

    Your SOCless administrator should be able to provide you with the ARN of the SOCless Lambda Execution Role,
    which you'll need when setting up your delegate IAM Role.

    To use this integration effectively, you'll need to be familiar with boto3's conventions for AWS service and operation names.
    You can refer to the boto3 documentation here to see those conventions for the service operation you wish to perform
    https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html

    !!! note
        - For a list of supported services_names, operations and operation_parameters,
          refer to https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/index.html
        - By default, this integration automatically paginates requests for APIs that return paginated results.
          This behaviour acts as a reasonable default. However, automatic pagination can exhaust certain resources,
          (eg. dynamodb scan API). If you need to disable_pagination for your use-case, set `disable_pagination=True`
        - This integration sets a default RoleSessionName of `SOClessAWSRequestIntegration` when it assume a delegate role. You can set your own RoleSessionName via the assume_role_config parameter

    Args:
        serivce_name: The boto3 name of the AWS service you want to make a request to. e.g s3
        operation: The boto3 client operation you want to perform, e.g put_object
        operation_parameters: Parameters for the operation. Required but can be empty dict for operations that don't take parameters
        assume_role_config: Configuration for the role to assume to perform the operation. See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sts.html#STS.Client.assume_role
            for a full list of values. Common values include `RoleArn`, `RoleSessionName` and `ExternalId`
        disable_pagination: Set to true to disable pagination
        save_to_vault: Determines if to save the results to the SOCless vault if the results are too large for step functions

    Returns:
        The integration always returns a dict.
        The structure of the dict varies based on the arguments passed to the function.
        However, three broad categories exist for the return type structure:

        **Category 1 - Non-Paginated Operation Mode:**

        When an operation is called in non-paginated mode,
        (either because the operation doesn't support pagination, or because `disable_pagination=True`),
        the dict object returned always exactly matches the boto3 response object for the operation.
        You can refer to the boto3 documentation for the operation to determine the response object structure

        **Category 2 - AWS Paginated Operations Mode:**

        For paginated operations, the dict object is of the structure

            {
                "ResultPages": [
                    <boto3 response object for the call>,
                    <boto3 response object for the call>,
                    ....
                ]
            }

        Where <boto3 response object> exactly matches the boto3 response object for the operation.

        **Category 3 - When `save_to_vault = true`:**

        When `save_to_vault=true` the actual response from the AWS Request
        is saved the SOCless vault, and references to their location in the vault
        are returned instead.
        Hence the response object is of the structure

            {
                "vault_id": "vault:{vault_file_id}",
                "file_id": "{vault_file_id}"
            }

        And the contents of in the vault_file with id {vault_file_id}
        is either a category 1 or 2 response depending on integration executed in
        non-paginated or paginated operation mode


    Example:

    Call S3 GetObject Operation using this integration
            ```
            {
                "service_name": "s3",
                "operation": "get_object",
                "operation_parameters": {
                    "Bucket": "bucket-name",
                    "Key": "/path/to/object"
                    },
                "assume_role_config": {
                    "RoleArn": "arn:aws:iam::[TARGET_ACCOUNT]:role/[TARGET_ROLE_NAME]"
                }
            }
            ```

    Call S3 PutObject Operation using this integration
            ```
            {
                "service_name": "s3",
                "operation": "put_object",
                "operation_parameters": {
                    "Bucket": "bucket-name",
                    "Key": "/path/to/object",
                    "Body": "Hello, world"
                    },
                "assume_role_config": {
                    "RoleArn": "arn:aws:iam::[TARGET_ACCOUNT]:role/[TARGET_ROLE_NAME]"
                }
            }

            ```
    """
    try:
        response = make_aws_request(
            service_name=service_name,
            operation=operation,
            operation_parameters=operation_parameters,
            assume_role_config=assume_role_config,
            disable_pagination=disable_pagination,
        )
        if save_to_vault:
            return vault.save_to_vault(json.dumps(response))
        else:
            return response
    except Exception as e:
        raise SoclessException(f"Error: {e}") from e


def lambda_handler(event, context):
    return socless_bootstrap(event, context, handle_state, include_event=False)
