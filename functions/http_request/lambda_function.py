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
from socless.exceptions import SoclessException
import requests
from decimal import Decimal


def handle_state(
    method: str,
    url: str,
    raise_for_status: bool = True,
    return_headers: bool = False,
    auth: list = [],
    **request_args,
) -> dict:
    """Make any HTTP request using the requests library.
    Full list of supported args is here: https://requests.readthedocs.io/en/latest/api/#requests.request

    Notes:
        Unable to return bytestring from this function, because it is not json serializable. Therefore
        response.content (a bytestring) will not be part of this lambda's return dict.

    Args:
        method : GET | POST | PUT | PATCH | DELETE
        url    : full url of the request destination
        raise_for_status : (optional) raise an HTTPError if request failed
        return_headers   : (optional) include a 'headers' key of the http_response headers in this lambda's return dict.
        auth             : (optional) Auth array to enable Basic/Digest/Custom HTTP Auth.
    Any other args will pass directly to requests.request(), such as:

        params:  (optional) Dictionary, list of tuples or bytes to send in the query string for the Request.
        data:    (optional) Dictionary, list of tuples, bytes, or file-like object to send in the body of the Request.
        json:    (optional) A JSON serializable Python object to send in the body of the Request.
        headers: (optional) Dictionary of HTTP Headers to send with the Request.

    Returns:
        Dict
        {
            "status_code": response.status_code,
            "headers": response.headers dictionary,
            "text": response content as UTF-8 string,
            "json" (OPTIONAL): response content as json, if valid json.
        }
    """
    if auth:
        if isinstance(auth, str):
            username, _, password = auth.partition(",")
            auth_tuple = (username.strip(), password.strip())
        elif isinstance(auth, list):
            auth_tuple = tuple(auth)
        elif isinstance(auth, tuple):
            auth_tuple = auth
        else:
            raise SoclessException(
                f"http_request `auth` parameter is not a list. type: {type(auth)}"
            )

        request_args["auth"] = auth_tuple

    response = requests.request(method=method, url=url, **request_args)

    if raise_for_status:
        response.raise_for_status()

    formatted_response = {
        "status_code": response.status_code,
        "text": response.text,
    }

    if return_headers:
        formatted_response["headers"] = response.headers

    try:
        formatted_response["json"] = response.json(parse_float=Decimal)
    except ValueError:
        print(f"No valid JSON returned from {method.upper()} {url}")

    return formatted_response


def lambda_handler(event, context):
    return socless_bootstrap(event, context, handle_state)
