# Setting up a Slack bot
Follow the steps below to setup a Slack bot for our tutorial:

1. In a web browser, log into your Slack instance
2. Navigate to https://api.slack.com/apps and hit `Create New App`
3. Enter a name for your application. The tutorial will use `socless-bot`
4. Select your development workspace. It should be the workspace you want your bot to be in
5. Hit Create app
6. On the "Basic Information" page for your app, click "Bots"
7. Click "Add Bot User"
8. Set a display name of your choice. We'll use `socless-bot`
9. Set a default username for your bot. We'll use `socless-bot`
10. Set "Always Show My Bot as Online" to "On"
11. Click "Add Bot User" again to save the changes
12. In the left sidebar, select "Oauth & Permissions"
13. Click "Install App to Workspace". Click "Authorize" to add the bot to your Slack Workspace
14. Once authorization is complete, you will be redirected back to the "Oauth & Permissions" page which will now display a "Bot User OAuth Access Token". Note this token down. Our integration will need this token
15. Log into your Slack instance in the Slack app. Click "Direct Messages" in the sidebar and search for your bot. Your bot should show up, ready for action.
16. Create a public channel in your Slack instance called "bat-signals". We'll need it for the rest of our tutorial.
17. Invite your Slack bot to the #bat-signals channel so that it can send messages to it


# Storing our Bots Credential for Use in SOCless
The current recommendation for storing credentials for use in the SOCless Framework is to use the AWS Systems Manager (SSM) Parameter Store service.
To store the bot token in SSM Parameter Store:

There are two methods to add your Slack bot token to ssm
## Method 1: Using the SOCless cli
This is currently the quickest method and relies on having the SOCless CLI installed

To add our bot token, execute the following command at a terminal

```bash
socless secret add
```

Then fill out the resulting prompt as such, using `/socless/slack/bot_token` for the Secret Path and the actual bot token for the `Secret Value`

## Method 2: Using the AWS UI
1. Log into your AWS Account and navigate to AWS SSM Manager in the SOCless region you wish
2. In the left sidebar of the Systems Manager page, select Parameters Store (you may need to scroll to see it)
3. On the Parameter Store page, click "Create Parameter"
4. Name your parameter /socless/slack/bot_token
5. Add a description for the parameter. We'll go with "Access token for SOCless Slack bot"
6. Under `Type`, select SecureString.
7. Under KMS Key ID select `alias/socless/lambdaKmsKey`
8. Under value, paste the `Bot User OAuth Access Token`
9. Click "Create Parameter"
Your bot token should now be encrypted and saved in AWS SSM Parameter Store under the name `/socless/slack/bot_token`. We'll specify that name in our serverless.yml file when we're configuring our integration for deployment
We're now set to write our Slack 'Send Message' Integration
