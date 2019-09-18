# Socless Core
Socless' core stack. Deploys Socless' core infrastructure and functions

# Requirements
- Node.js
- AWS account

# Setup

```
git clone git@github.com/twilio-labs/socless.git
cd socless
npm install
```

# Deployment

```
npm run [ dev | prod ]
```

# Stack Outputs

| Output                         | Type                | Description                                                              |
|--------------------------------|---------------------|--------------------------------------------------------------------------|
| LambdaVpcSG                    | Security Group ID   | Security group ID of the security group for Socless lambda functions       |
| PrivateFunctionSubnet          | VPC Subnet ID       | VPC Subnet ID for Socless private functions                                |
| AwaitMessageResponseActivity   | Activity Task ARN   | ARN of Activity Task used by Socless' Outbound message workflow            |
| EventsTable                    | DynamoDB Table Name | Name of Socless' Events Table                                              |
| MessageResponsesTable          | DynamoDB Table Name | Name of Socless' Message Responses Table                                   |
| LambdaKmsKey                   | KMS Key ID          | ID of KMS key used to encrypt environment variables for Lambda functions |
| SoclessVault                     | S3 Bucket Name      | Name of S3 bucket that serves' as Socless' Vault for storing large files   |
| PublicSubnet                   | VPC Subnet ID       | VPC Subnet ID for public-facing Lambda's and services                    |
| EIP                            | EIP Public IP       | Public IP address of Socless' EIP                                          |
| ServerlessDeploymentBucketName | S3 Bucket Name      | Name of S3 bucket which the Serverless framework uses to deploy Socless    |
| LambdaExecutionRoleArn         | IAM Role ARN        | ARN of default lambda execution role for Socless Lambda functions          |
| PlaybooksTable                 | DynamoDB Table Name | Name of Socless' Playbooks Table                                           |
| StatesExecutionRole            | IAM Role Name       | Name of IAM role used to execute state machines                          |
| ExecutionResultsTable          | DymamoDB Table Name | Name of the Execution Results Table                                      |
| LambdaExecutionRole            | IAM Role Name       | Name of the default lambda execution role for Socless Lambda functions     |
