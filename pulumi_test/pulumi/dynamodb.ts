import * as aws from '@pulumi/aws';

// DynamoDB tables
export const eventsTable = new aws.dynamodb.Table('socless_events', {
  attributes: [
    {
      name: 'id',
      type: 'S',
    },
  ],
  hashKey: 'id',
  readCapacity: 200,
  writeCapacity: 200,
});

export const executionResultsTable = new aws.dynamodb.Table('socless_execution_results', {
  attributes: [
    {
      name: 'execution_id',
      type: 'S',
    },
  ],
  hashKey: 'execution_id',
  readCapacity: 60,
  writeCapacity: 60,
});

export const messageResponsesTable = new aws.dynamodb.Table('socless_message_responses', {
  attributes: [
    {
      name: 'message_id',
      type: 'S',
    },
  ],
  hashKey: 'message_id',
  readCapacity: 50,
  writeCapacity: 50,
});

export const playbooksTable = new aws.dynamodb.Table('socless_playbooks', {
  attributes: [
    {
      name: 'StateMachine',
      type: 'S',
    },
  ],
  hashKey: 'StateMachine',
  readCapacity: 5,
  writeCapacity: 5,
});

export const customMappingsTable = new aws.dynamodb.Table('socless_custom_mappings', {
  attributes: [
    {
      name: 'key',
      type: 'S',
    },
  ],
  hashKey: 'key',
  readCapacity: 10,
  writeCapacity: 10,
});

export const dedupTable = new aws.dynamodb.Table('socless_dedup', {
  attributes: [
    {
      name: 'dedup_hash',
      type: 'S',
    },
  ],
  hashKey: 'dedup_hash',
  readCapacity: 50,
  writeCapacity: 50,
});
