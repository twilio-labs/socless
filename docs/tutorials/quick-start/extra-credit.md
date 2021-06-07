# Extra Credit
Want to put your new found skills to the test? Try adding a state to our Playbook that uses Twilio's SMS API to send the same message we send in our `Send_Slack_Message` state to your phone instead!

Here's some resources to help you:

- [Send an SMS Using Twilio API](https://www.twilio.com/docs/sms/api/message-resource#create-a-message-resource)
- [HTTPRequest Integration Reference Documentation](../../reference/builtin-integrations/http_request.md)


The answer to the challenge is shown below but give it a good go before viewing it


??? note "Extra Credit Solution"
    ```json hl_lines="31-46"
    {
      "Playbook": "[yourname]InvestigateLogin",
      "Comment": "Playbook to investigate a login",
      "StartAt": "Geolocate_IP",
      "States": {
        "Geolocate_IP": {
          "Type": "Task",
          "Resource": "${{self:custom.core.HTTPRequest}}",
          "Parameters": {
            "method": "GET",
            "url": "https://freegeoip.app/json/{{context.artifacts.event.details.ip}}"
          },
          "Next": "Send_Notification_To_Slack"
        },
        "Send_Notification_To_Slack": {
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
          "Next": "Send_SMS_Notification"
        },
        "Send_SMS_Notification": {
          "Type": "Task",
          "Resource": "${{self:custom.core.HTTPRequest}}",
          "Parameters": {
              "method": "POST",
              "url": "https://api.twilio.com/2010-04-01/Accounts/[your_twilio_account_sid]/Messages.json",
              "auth": [
                "[your_twilio_account_sid]",
                "{{secret('/socless/[yourname]/twilio_token')}}"
              ],
              "data": {
                "Body": "`{{context.artifacts.event.details.username}}` logged in from `{{context.results.Geolocate_IP.json.country_name}}` at coordinates `{{context.results.Geolocate_IP.json.latitude}}`, `{{context.results.Geolocate_IP.json.longitude}}`",
                "From": "[your_twilio_number]",
                "To": "{{secret('/socless/[yourname]/number')}}"
              }
            }
        }
      },
      "Decorators": {
        "TaskFailureHandler": {
          "Type": "Task",
          "Resource": "${{self:custom.core.HTTPRequest}}",
          "Parameters": {
            "method": "POST",
            "url": "https://slack.com/api/chat.postMessage",
            "json": {
              "channel": "#bat-signals",
              "text": "An error occurred in the our [yourname]InvestigateLogin playbook.\n ExecutionID: {{context.execution_id}} \n Error:\n ```{{context.errors}}```"
            },
            "headers": {
              "Authorization": "Bearer {{secret('/socless/slack/bot_token')}}"
            }
          },
          "End": true
        }
      }
    }
    ```
