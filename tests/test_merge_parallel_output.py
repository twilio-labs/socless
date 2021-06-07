from functions.merge_parallel_output import lambda_function

mock_parallel_steps_output = [
    {
        "execution_id": "12345-12345-123345",
        "artifacts": {
            "event": {
                "id": "0987-097987-098709",
                "created_at": "2021-03-01T18:00:24.736856Z",
                "data_types": {},
                "details": {"scan_name": "See If Any Detections"},
                "event_type": "Detections Occurred",
                "event_meta": {
                    "occured": "2021-11-25T09:00:00Z",
                    "datasource": "Some Datasource",
                    "description": "Some Event Description",
                },
                "investigation_id": "0987-097987-098709",
                "status_": "open",
                "is_duplicate": False,
                "playbook": "MockPlaybook",
            },
            "execution_id": "12345-12345-123345",
        },
        "State_Config": {
            "Name": "A_Parallel_Step",
            "Parameters": {
                "summary": "Dectections have happened",
            },
        },
        "results": {
            "A_Parallel_Step": {
                "id": "13467336",
            },
            "id": "13467336",
        },
    },
    {
        "execution_id": "12345-12345-123345",
        "artifacts": {
            "event": {
                "id": "0987-097987-098709",
                "created_at": "2021-03-01T18:00:24.736856Z",
                "data_types": {},
                "details": {"scan_name": "See If Any Detections"},
                "event_type": "detections occured",
                "event_meta": {
                    "occured": "2017-11-06T09:05:17Z",
                    "datasource": "Some Datasource",
                    "description": "Some Event Description",
                },
                "investigation_id": "0987-097987-098709",
                "status_": "open",
                "is_duplicate": False,
                "playbook": "MockPlaybook",
            },
            "execution_id": "12345-12345-123345",
        },
        "State_Config": {
            "Name": "Another_Parallel_Step",
            "Parameters": {
                "summary": "Something Was Detected",
            },
        },
        "results": {
            "Another_Parallel_Step": {
                "id": "123456789",
            },
            "id": "123456789",
        },
    },
]


def test_lambda_handler_returns_dict_if_event_is_empty_list():
    output = lambda_function.lambda_handler(mock_parallel_steps_output, {})
    expected_output = {
        "execution_id": "12345-12345-123345",
        "artifacts": {
            "event": {
                "id": "0987-097987-098709",
                "created_at": "2021-03-01T18:00:24.736856Z",
                "data_types": {},
                "details": {"scan_name": "See If Any Detections"},
                "event_type": "detections occured",
                "event_meta": {
                    "occured": "2017-11-06T09:05:17Z",
                    "datasource": "Some Datasource",
                    "description": "Some Event Description",
                },
                "investigation_id": "0987-097987-098709",
                "status_": "open",
                "is_duplicate": False,
                "playbook": "MockPlaybook",
            },
            "execution_id": "12345-12345-123345",
        },
        "State_Config": {
            "Name": "Another_Parallel_Step",
            "Parameters": {"summary": "Something Was Detected"},
        },
        "results": {
            "A_Parallel_Step": {"id": "13467336"},
            "id": "123456789",
            "Another_Parallel_Step": {"id": "123456789"},
        },
    }
    assert output == expected_output


# def test_lambda_handler_returns_dict_from_combined_list():
#     event_list = [
#         {"first_item": "foo"},
#         {"second_item": {"sub_item": "bar"}},
#         {"second_item": {"sub_item": "baz"}},
#     ]
#     output = lambda_function.lambda_handler(event_list, {})

#     assert output == {"first_item": "foo", "second_item": "bar", "third_item": "baz"}


# # https://docs.pytest.org/en/stable/monkeypatch.html
# def test_handle_state_with_monkeypatch_to_prevent_failure_of_external_api_call(
#     monkeypatch,
# ):
#     expected_telegram_message = "ATTN DR ELIAS KRONISH -STOP-  WE ARE LOOKING FORWARD TO THE ANNUAL CHRISTMAS PARTY -STOP- "

#     # The REAL lambda_function.send_telegram function returns a bool True
#     #  when it succeeds, so we replicate that here too.
#     def mock_send_telegram(telegram):
#         assert telegram == expected_telegram_message
#         return True

#     # assign our mock send telegram function to overwrite the real send_telegram in this test
#     monkeypatch.setattr(lambda_function, "send_telegram", mock_send_telegram)

#     # run the now modified handle_state
#     send_telegram_lambda_output = handle_state(
#         "Elias Kronish", "we are looking forward to the annual christmas party."
#     )
#     assert send_telegram_lambda_output["telegram"] == expected_telegram_message
