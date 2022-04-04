import * as pulumi from '@pulumi/pulumi';
import * as aws from '@pulumi/aws';
import * as awsx from '@pulumi/awsx';
import { FULL_NAME } from './utils';

// S3 Buckets
export const vaultBucket = new aws.s3.Bucket(`${FULL_NAME}-vault`, {
  lifecycleRules: [
    {
      enabled: true,
      expiration: {
        days: 1,
      },
      prefix: 'one_day_temp/',
    },
  ],
  tags: {
    Name: 'Socless Vault',
  },
});

export const logsBucket = new aws.s3.Bucket(`${FULL_NAME}-logs`, {
  lifecycleRules: [
    {
      enabled: true,
      expiration: {
        days: 365,
      },
    },
  ],
  tags: {
    Name: 'Socless Logs',
  },
});
