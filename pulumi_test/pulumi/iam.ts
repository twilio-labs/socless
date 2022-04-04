import * as pulumi from '@pulumi/pulumi';
import * as aws from '@pulumi/aws';
import * as awsx from '@pulumi/awsx';
import { accountID, FULL_NAME, stackToRegion } from './utils';
import { PolicyDocument } from '@pulumi/aws/iam';

const integrationPolicy: PolicyDocument = {
  Version: '2012-10-17',
  Statement: [
    {
      Effect: 'Allow',
      Action: 'sts:AssumeRole',
      Resource: '*',
    },
  ],
};

export const lambdaExecutionRole = new aws.iam.Role(`${FULL_NAME}-default-lambda-execution`, {
  assumeRolePolicy: {
    Version: '2012-10-17',
    Statement: [
      {
        Effect: 'Allow',
        Principal: {
          Service: ['lambda.amazonaws.com', 'apigateway.amazonaws.com'],
        },
        Action: 'sts:AssumeRole',
      },
    ],
  },
  managedPolicyArns: [
    'arn:aws:iam::aws:policy/AmazonAPIGatewayInvokeFullAccess',
    'arn:aws:iam::aws:policy/AmazonDynamoDBFullAccess',
    'arn:aws:iam::aws:policy/service-role/AWSLambdaDynamoDBExecutionRole',
    'arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole',
    'arn:aws:iam::aws:policy/AWSLambdaInvocation-DynamoDB',
    'arn:aws:iam::aws:policy/AWSStepFunctionsFullAccess',
    'arn:aws:iam::aws:policy/service-role/AWSLambdaVPCAccessExecutionRole',
    'arn:aws:iam::aws:policy/AmazonS3FullAccess',
    'arn:aws:iam::aws:policy/AmazonSESFullAccess',
    'arn:aws:iam::aws:policy/AmazonSSMReadOnlyAccess',
  ],
  inlinePolicies: [
    {
      name: `${FULL_NAME}-aws-request-integration-policy`,
      policy: JSON.stringify(integrationPolicy),
    },
  ],
});

export const statesExeuctionRole = new aws.iam.Role(`${FULL_NAME}-states-execution`, {
  assumeRolePolicy: {
    Version: '2012-10-17',
    Statement: [
      {
        Effect: 'Allow',
        Principal: {
          Service: `states.${stackToRegion()}.amazonaws.com`,
        },
        Action: 'sts:AssumeRole',
      },
      {
        Effect: 'Allow',
        Principal: {
          Service: 'events.amazonaws.com',
        },
        Action: 'sts:AssumeRole',
      },
    ],
  },
});
