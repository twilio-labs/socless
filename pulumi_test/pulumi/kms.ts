import * as pulumi from '@pulumi/pulumi';
import * as aws from '@pulumi/aws';
import * as awsx from '@pulumi/awsx';
import { accountID, FULL_NAME } from './utils';
import { lambdaExecutionRole } from './iam';

const keyPolicy = {
  Version: '2012-10-17',
  Id: 'policy',
  Statement: [
    {
      Sid: 'Allow administration of the key',
      Effect: 'Allow',
      Action: [
        'kms:Create*',
        'kms:Describe*',
        'kms:Enable*',
        'kms:List*',
        'kms:Put*',
        'kms:Update*',
        'kms:Revoke*',
        'kms:Disable*',
        'kms:Get*',
        'kms:Delete*',
        'kms:ScheduleKeyDeletion',
        'kms:CancelKeyDeletion',
      ],
      Principal: {
        AWS: [`arn:aws:iam::${accountID}:root`],
      },
      Resource: '*',
    },
    {
      Sid: 'Allow Lambda Decryption',
      Effect: 'Allow',
      Action: ['kms:Decrypt'],
      Principal: {
        AWS: lambdaExecutionRole.arn,
      },
      Resource: '*',
    },
    {
      Sid: 'Allow Administrator usage of key',
      Effect: 'Allow',
      Action: ['kms:Decrypt', 'kms:Encrypt'],
      Principal: {
        AWS: [`arn:aws:iam::${accountID}:root`],
      },
      Resource: '*',
    },
  ],
};

// Create a new KMS key
export const lambdaKey = new aws.kms.Key(`${FULL_NAME}-lambda-env-encryption-key`, {
  description: 'KMS Key for encrypting Lambda variables',
  isEnabled: true,
  enableKeyRotation: true,
  policy: JSON.stringify(keyPolicy),
});

// Create a new alias to the key
export const lambdaKeyAlias = new aws.kms.Alias('alias/socless/lambdaKmsKey', {
  targetKeyId: lambdaKey.keyId,
});
