import * as pulumi from '@pulumi/pulumi';
import { buildIntegrationTag, registerAutoTags, tagSoclessPlatform } from './utils';

// Run this before any resources are created to ensure default tags get added
registerAutoTags({
  'user:Project': pulumi.getProject(),
  'user:Stack': pulumi.getStack(),
  ...tagSoclessPlatform,
  ...buildIntegrationTag('core'),
});

import { logsBucket, vaultBucket } from './s3';
import {
  customMappingsTable,
  dedupTable,
  eventsTable,
  executionResultsTable,
  playbooksTable,
} from './dynamodb';
import { apig } from './apig';
import { lambdaKeyAlias, lambdaKey } from './kms';
import { lambdaExecutionRole, statesExeuctionRole } from './iam';
import { awaitMessageResponseActivity, saveMessageResponseTaskTokenMachine } from './sfn';
import { playbookLogsGroup } from './logs';

// outputs from the socless core project, can be imported by other projects
export const soclessCoreProject = {
  buckets: {
    vault: vaultBucket,
    logs: logsBucket,
  },
  tables: {
    results: executionResultsTable,
    dedup: dedupTable,
    events: eventsTable,
    mappings: customMappingsTable,
    playbooks: playbooksTable,
  },
  api: apig,
  kms: {
    key: lambdaKey,
    alias: lambdaKeyAlias,
  },
  iam: {
    lambdaExecutionRole: lambdaExecutionRole,
    statesExecutionRole: statesExeuctionRole,
  },
  sfn: {
    awaitMessageResponseActivity: awaitMessageResponseActivity,
    saveMessageResponseTaskToken: saveMessageResponseTaskTokenMachine,
  },
  logs: {
    playbookLogs: playbookLogsGroup,
  },
};

// export = async () => {
//   const current = await aws.getCallerIdentity({});
//   console.log(current.accountId)
// }
// const accountId = current.then(current => {

//   console.log(current.accountId)
//   return current.accountId

// });
