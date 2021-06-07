# Testing Our Endpoint
We're now ready to test our complete workflow.

Since we don't actually have a ~~high frequency generator-receiver~~ detection system, we'll use `curl` to simulate one.

Open your terminal and execute the command below, making sure to replace `$AUTH_TOKEN` and `$ENDPOINT_URL` with their actual values

!!! tip
    If you set `AUTH_TOKEN` and `ENDPOINT_URL` as environment variables on your machine, you'll be able to copy-paste and execute the below command as is. You can do so by first executing
    ```
    AUTH_TOKEN=[your-auth-token] ENDPOINT_URL=[your-endpoint-url]
    ```
    at the terminal before running the command below


```
curl -H "Authorization: $AUTH_TOKEN" \
    -X POST $ENDPOINT_URL \
    -d @functions/tutorial_endpoint/test_case.json
```

If the request succeeds, you should get a message in your #bat-signals Slack channel.

And that's it! We've successfully created an Endpoint that can trigger our SOCless Playbook!
