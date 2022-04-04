import * as pulumi from '@pulumi/pulumi';
import * as aws from '@pulumi/aws';
import * as awsx from '@pulumi/awsx';
import { FULL_NAME } from './helpers';

// Security Groups
export const soclessLambdaVpcSG = new aws.ec2.SecurityGroup(`${FULL_NAME}-securitygroup`, {
  tags: {
    Name: 'Socless Lambda SG',
  },
});
