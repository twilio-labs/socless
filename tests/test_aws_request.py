from functions.aws_request.lambda_function import (
    make_boto_response_json_serializable,
    call_service_operation,
    make_service_client,
    assume_role,
    make_aws_request,
    determine_operation_handler,
    call_service_operation_with_pagination,
    handle_state,
)

from conftest import mock_vault_objects_mapping
import io
import os
from botocore.response import StreamingBody
import boto3
from datetime import datetime
import pytest
from socless.exceptions import SoclessException
from moto import mock_iam, mock_sts, mock_s3


def test_make_boto_response_json_serializable_succeeds():
    test_string = "hello world"
    test_int = 1
    test_bool = True
    test_none = None
    test_float = 1.0
    streaming_body_bytes = bytes(test_string, "utf-8")
    test_streaming_body = StreamingBody(
        io.BytesIO(streaming_body_bytes), len(streaming_body_bytes)
    )
    test_list = [test_string, test_int, test_float]

    test_datetime = datetime(2016, 6, 23)

    test_dict = {
        "str": test_string,
        "int": test_int,
        "float": test_float,
        "bool": test_bool,
        "None": test_none,
        "datetime": test_datetime,
        "list": test_list,
        "dict": {
            "str": test_int,
            "int": test_int,
            "datetime": test_datetime,
            "StreamingBody": test_streaming_body,
        },
    }

    expected_output = {
        "str": test_string,
        "int": test_int,
        "float": test_float,
        "bool": test_bool,
        "None": test_none,
        "datetime": str(test_datetime),
        "list": test_list,
        "dict": {
            "str": test_int,
            "int": test_int,
            "datetime": str(test_datetime),
            "StreamingBody": test_string,
        },
    }
    assert make_boto_response_json_serializable(test_dict) == expected_output


def test_make_service_client_returns_the_correct_client_type():
    sample_services = ["s3", "ssm", "stepfunctions", "dynamodb"]
    for service in sample_services:
        assert str(type(make_service_client(service))) == str(
            type(boto3.client(service))
        )

    # Sanity check here to make sure that boto3 client types are actually different.
    # If this check fails, then it means boto3 has changed their client logic (likely to return a generic client type) regardless of service
    # rendering the above test useless
    assert str(type(boto3.client("ssm"))) != str(type(boto3.client("stepfunctions")))


def test_make_service_client_raises_socless_exception_for_invalid_service_name():
    with pytest.raises(SoclessException):
        make_service_client("thisisnotanawsserviceunlessawshasgonenuts")


def test_determine_operation_handler_returns_correct_handler():
    # Using S3 client as the test case here but these tests
    s3_client = boto3.client("s3")

    put_object_pagination_disabled = determine_operation_handler(
        client=s3_client,
        operation="put_object",
        pagination_disabled=True,
    )

    put_obect_without_pagination_disabled = determine_operation_handler(
        client=s3_client,
        operation="put_object",
        pagination_disabled=False,
    )
    # S3 put_object should always get the call_service_operation handler regardless of disable_pagination
    # because put_object is an unpageable call
    assert (
        put_object_pagination_disabled
        == put_obect_without_pagination_disabled
        == call_service_operation
    )

    list_object_pagination_disabled = determine_operation_handler(
        client=s3_client, operation="list_objects_v2", pagination_disabled=True
    )

    list_objects_without_pagination_disabled = determine_operation_handler(
        client=s3_client, operation="list_objects_v2", pagination_disabled=False
    )

    # list_objects_v2 should return call_service_operation if pagination_disabled
    assert list_object_pagination_disabled == call_service_operation

    # list_objects_v2 should return call_service_operation_with_pagination if pagination_disabled is False
    assert (
        list_objects_without_pagination_disabled
        == call_service_operation_with_pagination
    )

    # Sanity check to ensure that both functions don't actually look the same when compared
    assert list_object_pagination_disabled != list_objects_without_pagination_disabled


@mock_sts
def test_handle_state_works_using_s3_get_object_example():
    mock_key, mock_value = list(mock_vault_objects_mapping().items())[0]

    response = handle_state(
        service_name="s3",
        operation="get_object",
        operation_parameters={
            "Bucket": os.environ["SOCLESS_VAULT"],
            "Key": mock_key,
        },
        assume_role_config={
            "RoleArn": f"arn:aws:iam::{os.environ['MOTO_ACCOUNT_ID']}:role/test123"
        },
    )

    assert response["Body"] == mock_value


@mock_sts
def test_handle_state_works_saves_to_vault():
    mock_key, mock_value = list(mock_vault_objects_mapping().items())[0]

    response = handle_state(
        service_name="s3",
        operation="get_object",
        operation_parameters={
            "Bucket": os.environ["SOCLESS_VAULT"],
            "Key": mock_key,
        },
        assume_role_config={
            "RoleArn": f"arn:aws:iam::{os.environ['MOTO_ACCOUNT_ID']}:role/test123"
        },
        save_to_vault=True,
    )

    assert set(response.keys()) == set(["vault_id", "file_id"])
