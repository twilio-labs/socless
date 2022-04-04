import * as pulumi from '@pulumi/pulumi';
import * as aws from '@pulumi/aws';
import * as awsx from '@pulumi/awsx';

export const playbookLogsGroup = new aws.cloudwatch.LogGroup('/socless/playbook-execution-logs');
