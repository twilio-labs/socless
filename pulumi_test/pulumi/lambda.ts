import * as aws from '@pulumi/aws';
import { FunctionArgs } from '@pulumi/aws/lambda';
import { lambdaExecutionRole } from './iam';
import { soclessVpcExports } from './vpc';
import { vaultBucket } from './s3';
import { dedupTable, eventsTable, executionResultsTable, messageResponsesTable } from './dynamodb';
import { newSoclessLambda, registerLambdaDefaults } from './utils';
import { awaitMessageResponseActivity } from './sfn';

const { privateFunctionSubnet, sg } = soclessVpcExports;

export const defaultEnvVars = {
  SOCLESS_VAULT: vaultBucket.bucket,
  SOCLESS_RESULTS_TABLE: executionResultsTable.name,
  SOCLESS_DEDUP_TABLE: dedupTable.name,
  SOCLESS_EVENTS_TABLE: eventsTable.name,
};

const defaultLambdaArgs: FunctionArgs = {
  role: lambdaExecutionRole.arn,
  handler: 'lambda_function.lambda_handler',
  runtime: 'python3.7',
  timeout: 30,
  memorySize: 128,
  vpcConfig: {
    securityGroupIds: [sg.id],
    subnetIds: [privateFunctionSubnet.id],
  },
  environment: { variables: defaultEnvVars },
};

registerLambdaDefaults(defaultLambdaArgs);

// TODO: figure out how pulumi shares resources, do we want to more strongly type this?
export const functions = {
  // TODO: add archive path support to this helper function
  ...newSoclessLambda('http_request', defaultLambdaArgs),
  ...newSoclessLambda('_merge_parallel_output', defaultLambdaArgs),
  ...newSoclessLambda('_socless_save_msg_resp_token', {
    ...defaultLambdaArgs,
    environment: {
      variables: {
        ...defaultEnvVars,
        AWAIT_MESSAGE_RESPONSE_ARN: awaitMessageResponseActivity.name,
        MESSAGE_RESPONSES_TABLE: messageResponsesTable.name,
      },
    },
  }),
  ...newSoclessLambda('_playground', defaultLambdaArgs),
  ...newSoclessLambda('_socless_counter', defaultLambdaArgs),
  ...newSoclessLambda('set_investigation_status', defaultLambdaArgs),
  ...newSoclessLambda('add_custom_mapping', {
    ...defaultLambdaArgs,
    environment: {
      variables: { ...defaultEnvVars },
    },
  }),
};
