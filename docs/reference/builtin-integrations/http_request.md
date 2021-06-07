# HTTPRequest Integration

The HTTPRequest Integration enables users make arbitrary HTTP requests to any API.

It is based on the [Python Requests](https://2.python-requests.org/en/master/api/#main-interface)

Below are some examples of how you might use the Integration

=== "Simple GET Request"
    ```
    {
      "Type": "Task",
      "Resource": "${{self:custom.core.HTTPRequest}}",
      "Parameters": {
        "method": "GET",
        "url": "https://freegeoip.app/json/{{context.artifacts.event.details.ip}}"
      },
      "Next": "Next_State"
    }
    ```

=== "GET Request with URL Query Params"
    ```
    {
      "Type": "Task",
      "Resource": "${{self:custom.core.HTTPRequest}}",
      "Parameters": {
        "method": "GET",
        "url": "https://freegeoip.app/json/{{context.artifacts.event.details.ip}}",
        "params": {
          "name": "Bruce Wayne",
          "Alias": "unknown"
        }
      },
      "Next": "Next_State"
    }
    ```

=== "POST Request With Headers & json payload"
    ```
    {
      "Type": "Task",
      "Resource": "${{self:custom.core.HTTPRequest}}",
      "Parameters": {
        "method": "POST",
        "url": "https://slack.com/api/chat.postMessage",
        "json": {
          "channel": "#bat-signals",
          "text": "`{{context.artifacts.event.details.username}}` logged in from `{{context.results.Geolocate_IP.json.country_name}}` at coordinates `{{context.results.Geolocate_IP.json.latitude}}`, `{{context.results.Geolocate_IP.json.longitude}}`"
        },
        "headers": {
          "Authorization": "Bearer {{secret('/socless/slack/bot_token')}}"
        }
      },
      "End": true
    }
    ```

=== "Basic Auth"
    ```
    {
      "Type": "Task",
      "Resource": "${{self:custom.core.HTTPRequest}}",
      "Parameters": {
        "method": "GET",
        "url": "https://freegeoip.app/json/{{context.artifacts.event.details.ip}}",
        "auth": ["{{secret('socless/foo/bar/user')}}", "{{secret('/socless/foo/bar/password')}}"]
      },
      "Next": "Next_State"
    }
    ```

!!! danger
    **The HTTPRequest Integration does not support paginated requests. Do NOT use it with APIs that return paginated results. Write a custom integration instead**

::: functions.http_request.lambda_function.handle_state
