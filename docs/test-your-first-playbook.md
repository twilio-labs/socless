To test our playbook, we'll use curl to send our alert. You may use any other HTTP request sending tool you’re comfortable with.

Here's the alert payload we'll be sending

```
{
  "alert_name": "Suspicious Login Detected",
  "response_plan": "InvestigateLogin",
  "details": [
    {
      "username": "bruce.wayne",
      "ip": "113.63.125.3"
    }
  ]
}
```

If you’re sticking with curl, save that payload in the `investigate_login` folder in a file called `test_case.json`. Then execute the below curl command from the root of your `socless-playbooks` repository to send the payload to your Event Endpoint. Be sure to replace {endpoint-url} with your action endpoint URL.

```
curl -X POST {endpoint-url} -d @playbooks/investigate_login/test_case.json
```

Once the request completes, you should receive a message in the #bat-signals channel. Furthermore, the AWS Step Functions console will show the execution history for your playbook.

Congratulations! You've successfully completed your first playbook 🍾 

Keep on learning by heading to the tutorial on [Interacting with Humans in Slack](./Tutorial:-Interacting-with-Humans-via-Slack)
