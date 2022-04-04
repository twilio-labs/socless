import * as pulumi from '@pulumi/pulumi';
import * as aws from '@pulumi/aws';
import * as awsx from '@pulumi/awsx';

// Define an endpoint that invokes a lambda to handle requests
export const apig = new aws.apigateway.RestApi('api', {
  name: 'socless',
});
