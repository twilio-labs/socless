# Configuring Secrets
## Creating a Secret for Our Endpoint
While there are many many ways to generate a secret for our SOCless endpoint, we'll go with something simple.

Run the following snippet in your terminal
```bash
python3 -c 'import secrets; print(secrets.token_hex(16))'
```
This should generate a random, 32 character string. We'll use this as our endpoint's `AUTH_TOKEN`. Copy it to your clipboard then keep it somewhere private but recoverable for two reasons:

1. We'll need it to successfully make requests to our endpoint
2. Anyone who has this token can make a request to our endpoint and we don't want that

Once we've saved our token somewhere secure, we'll need to upload it to SOCless as well so that our Endpoint can use it after its deployed.

Next, let's add the authentication token as a secret in SOCless

## Uploading Our Secret


At the terminal execute the following command
```bash
socless auth login
socless secret add
```

Answer the resulting prompts as follows

* `Target Environment (sandbox, dev, stage, prod):` sandbox
* `Secret Path (Must begin with /socless/):` /socless/[yourname]/tutorial_endpoint_token

    --8<-- "docs-snippets/replace_yourname.md"


* `Secret Value:` (paste the token you generated here)
* `Description:` Authentication token for my socless tutorial endpoint
* `💥 Overwrite credential if it exist? [y/N]:` y

Our authentication token has now been uploaded to SOCless!

In the next section, where we configure our endpoint for deployment, we'll configure this secret as an environment variable for our endpoint function.
