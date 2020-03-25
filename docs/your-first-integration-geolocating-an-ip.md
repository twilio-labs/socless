# Your First Integration: Geolocate IP
Socless uses Integrations to take actions within playbooks. An Integration is an AWS Lambda functions that uses the `socless_bootstrap` function from the Socless Python library to manage its execution life-cycle (i.e fetching its inputs and saving its outputs). Integrations typically integrate with 3rd party APIs – hence the name 'Integrations' – to accomplish a task.

The bare-bones, pseudo-code implementation for any Socless integration is shown below

```
from socless import socless_bootstrap

def handle_state(param1, param2, …):
	"""Core action logic goes here"""
	# Implement core actions (e.g api requests) and return dictionary with desired results
	return {…}

def lambda_handler(event, lambda_context):
	"""Handles life-cycle of handle_state’s execution"""
	return socless_bootstrap(event, lambda_context, handle_state, include_event=False)
```

The `socless_bootstrap` function takes the below parameters:

| Parameter      | Description                                                                                                                                                                                                                                                                                                                                  | Required? | Default |
|----------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-----------|---------|
| event          | Payload containing information the Integration needs to execute. Passed in either by an executing playbook or by a developer during testing.                                                                                                                                                                                                 | Yes       | N/A     |
| handle_state   | A function that implements the core logic of the Integration. Must return a dictionary                                                                                                                                                                                                                                                       | Yes       | N/A     |
| include_event  | Boolean to specify if the whole playbook execution context (not lambda_context) should be made available to the handle_state function during its execution. Typically set to `True` for integrations that need to refer to elements of execution context in string templates. If `True` param1 of handle_state must be the keyword `context` | No        | FALSE   |
| lambda_context | The Lambda context object passed in by AWS whenever it triggers a Lambda function                                                                                                                                                                                                                                                            | Yes       | N/A     |

In this tutorial, we'll learn the basics of Integration development by writing one that geolocates an IP address and returns its country, latitude and longitude.

## Setting Up
To begin, change out of socless directory at your command-line (if you’re still within it) to a higher-level project folder.

Next, run the commands below to download the `socless-integrations-template` which contains the pre-configurations we need for developing our Integration

```
git clone git@github.com:twilio-labs/socless-integrations-template.git socless-tutorial
cd socless-tutorial
./setup
virtualenv --python=python3.7 venv
source venv/bin/activate
```

The commands:

* clone the socless-integrations-template into a folder named `socless-tutorial`
* run a setup script that installs the development dependencies we need (serverless framework and relevant plugins) then deletes the setup script.
* create and activate a Python 3.7 virtual environment which will be used to package our Integration when we're ready to deploy it.

After running the commands, you should be left with a `socless-tutorial` directory that contains a `functions` folder. This folder is where the code for our tutorial Integrations will live.

Now that we're setup, let's code our Integration

## Coding the GeoIP Integration
For IP address geolocation, we’ll rely on [https://tools.keycdn.com/geo.json](https://tools.keycdn.com/geo.json) which is a free geolocation API that requires no auth keys. This allows us keep things simple. Click the link to get an idea of the data the API returns.

The geolocation logic for our integration will:

* be implemented in a `handle_state` function that only needs an IP as a parameter.
* use the python requests library to perform a GET request to https://tools.keycdn.com/geo.json with the url parameter `host={ip}`
* return a dictionary containing the country name, city name, latitude and longitude of the IP address.

Our Integration will have a `lambda_handler` function that

* serves as AWS Lambda's entry point for our integration
* invokes `socless_bootstrap` to manage its life-cycle
* return the results of socless_bootstrap

Here’s what the implementation of the integration described above looks like
```
import requests
from socless import socless_bootstrap

def handle_state(ip):
    r = requests.get("https://tools.keycdn.com/geo.json", params={"host": ip})
    geoip_info = r.json()['data']['geo']
    desired_results = {
        "country": geoip_info['country_name'],
        "latitude": str(geoip_info['latitude']),
        "longitude": str(geoip_info['longitude'])
        }
    return desired_results


def lambda_handler(event, context):
    return socless_bootstrap(event, context, handle_state)

```

In the `socless-tutorial/functions` directory, create a subdirectory called `geoip` and save the implementation in a file called `lambda_function.py`. That’s all the code we need to write for our Integrations logic.

## Specify Dependencies
Notice that our integration makes use of the Python `requests` library which isn’t one of the libraries pre-packaged with AWS Lambda. As such, we’ll need to specify `requests` as a dependency with our deployment package. To do so, open the pre-existing `requirements.txt` file in the functions directory, and add requests at the bottom of the file. Your file should end up looking like this:

```
git+https://github.com/twilio-labs/socless_python.git#egg=socless
requests
```
The first dependency in the file is the Socless Python library that provides the `socless_bootstrap` function. Any dependency listed in the `functions/requirements.txt` file gets deployed will all functions in the `functions` folder. To learn more about configuring dependencies for functions, visit the [Socless & Serverless](socless-and-serverless.md) documentation page

Our integration’s implementation is complete and our dependencies have been specified. The last thing we need to do is configure the function for deployment.

## Configuring our integration for Deployment
Socless Integrations are deployed using the Serverless Framework. To deploy our integration, open the `serverless.yml` file and configure a function that:

* is reference-able in our config as `GeoIP`
* is named `socless_tutorial_geoip`
* has a handler at `lambda_function.lambda_handler`
* has the description: "Integration to geolocate an IP address"
* creates its source package from `functions/geoip`

Here's what that configuration looks like:
```
functions:
  GeoIP:
    name: socless_tutorial_geoip
    handler: lambda_function.lambda_handler
    description: Integration to geolocate an ip
    package:
      include:
        - functions/geoip
```

Next, we need to ensure that the AWS ARN of the function is output from the deployment stack after deployment. Doing so will allow the arn to be referenced by the playbook we will write shortly. To accomplish this, include the below configuration in the `serverless.yml` file, starting on the same indentation level as the `functions` key-word in the file

```
resources:
  Outputs:
    GeoIP:
      Description: ARN of GeoIP integration
      Value:
        Fn::Sub: ${GeoIPLambdaFunction.Arn}		
```

 With that, our Integration is fully configured for deployment.

## Deploying the Integration
If your Python 3.7 virtual environment is no longer active, reactivate it by running the command `. venv/bin/activate` from within your socless-tutorial directory.

Now, deploy the integration be executing:

```
npm run dev
```

Once the deployment is complete, you should see the ARN for the Integration's Lambda function displayed. You don't need to note this ARN down as we'll reference it by the `GeoIP` name whenever we need it.

## Testing the Integration
Log into the AWS console, navigate to the Lambda service in your Socless dev region, and open the Lambda function for the integration we just deployed (socless_tutorial_geoip).

Click `Test`, and configure the below test event:
```
{
	"_testing": true,
	"State_Config": {
		"Name": "Test_State",
		"Parameters": {
			"ip": "113.63.125.3"
		}
	}
}
```
Observe that the key-value pair in the `Parameters` object maps exactly to the parameters we specified for the `handle_state` function of our integration. This test event simulates a small subset of the data that the integration would receive when it's called by an actual playbook execution.

Give the test event any name of your choosing then hit create.
Once the test event is created, click `Test` to test the integration. If the test executes successfully, you'll have an Execution result like below which shows the test event and the resulting geolocated IP in a `results` object.

```
{
  "_testing": true,
  "State_Config": {
    "Name": "Test_State",
    "Parameters": {
      "ip": "113.63.125.3"
    }
  },
  "results": {
    "country": "China",
    "latitude": '29.65',
    "longitude": '91.1'
  }
}
```
Feel free to change the IP address in your test case and play around a little.

## Conclusion
Congratulations! You've written, deployed and tested your first integration! Pat yourself on the back, take a breather, then head to the next page to write your second integration
