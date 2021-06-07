# Introduction
SOCless is deployed using the [Serverless Framework](https://serverless.com).

SOCless uses the Serverless Framework as its orchestration technology. All the core infrastructure that powers SOCless is deployed via a single Serverless Framework application. Additional functionality (Playbooks, Integrations, Endpoints, etc) are deployed via their own Serverless Framework applications. This means that SOCless is designed to be modular and is deployed as such. In this documentation, we'll deploy SOCless' core infrastructure. Later documentation will cover the deployment of additional SOCless modules like integrations.

Pre-requisites

* An AWS Account
* The [Serverless Framework installed](https://serverless.com/framework/docs/providers/aws/guide/installation/)
* The [aws-cli](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-install.html) installed
* An [aws-cli profile configured with access keys](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration)
* Python 3.7, pip and git


Once the pre-requisites have been successfully set up, move to the next section

# Clone socless
Start by cloning the SOCless repository to any directory on your local machine that you've designated for code projects using the command below:

```
git clone git@github.com:twilio-labs/socless.git
```

Change into the cloned directory and install the deployment dependencies by running the below command

```
npm install
```

Finally, setup and activate a Python3.7 virtual environment using the commands below.

```
virtualenv --python=python3.7 venv
. venv/bin/activate
```
Keep the virtual environment active for the rest of the tutorial

# Specify AWS Profile
Open the package.json file contained in the cloned folder. In the `config` object, set the `aws_profile` value to match the name of the AWS CLI profile you configured at the start of the guide. For example, If your configured profile was named `default`, the `config` object should look like this:

```
"config":{
    "aws_profile": "default",
    "dev": "--stage dev --region us-west-2",
    "prod": "--stage prod --region us-east-1"
}
```
# (Optional) Modify Development/Production environment Config

By default, SOCless supports a development and production environment. The development environment, (dev) is set to AWS us-west-2 region, and the Production environment (prod) is AWS us-east-1 region. If you do not wish to change the deployment regions, you can skip to Deploy section.

If you want to use different regions for dev/prod, change the region specified for them in the config object. For example, the below config uses us-east-2 for dev and us-west-2 for prod.

```
"config":{
    "aws_profile": "default",
    "dev": "--stage dev --region us-east-2",
    "prod": "--stage prod --region us-west-2"
}
```
However, before changing regions, we recommend you review the [AWS Region Table](https://aws.amazon.com/about-aws/global-infrastructure/regional-product-services/) to ensure that the region you want to use supports all AWS services you may want to integrate with down the line (e.g Amazon SES)

# Deploy socless to dev/prod
Run the following command within the socless directory to deploy socless dev environment:

```
npm run dev
```
Run the following command within socless directory to deploy socless prod environment:
```
npm run prod
```
Both commands are used to deploy *AND redeploy* SOCless to the dev and prod environments respectively after changes have been made.

# Review the Deployment Output
The Serverless Framework deploys applications to AWS using the AWS Cloudformation service. Each Serverless application is deployed as a CloudFormation Stack.
If the SOCless deployment succeeded, your terminal should show Cloudformation Stack Outputs of the deployed resources. Additionally, if you log into the AWS console and navigate to the Cloudformation service in the region you deployed SOCless to, you should find a Cloudformation stack named `socless-

With SOCless successfully deployed, you're ready to write [your first playbook](tutorials/quick-start/introduction.md)
