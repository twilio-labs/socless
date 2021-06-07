import pytest
from functions.http_request import lambda_function


def test_handle_state():
    pass


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
