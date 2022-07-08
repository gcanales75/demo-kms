# Security Best Practices - KMS Demo (boto3)

In this demo you will demonstrate how to perform encrypt/decript operations on *strings* using AWS Key Management Service (KMS) and DynamoDB

Diagram:

![diagram1](images/kms-demo.drawio.png)

## Setting up the environment

1. Create a KMS Customer managed keys, since it will not be used in a AWS service. Use this opportunity to explain the difference KMS options in the console.

    KMS key creation parameters:

    - Key type: Symmetric

    - Key usage: Encrypt and decrypt

    - Alias: `demo-kms`

    - Key administrator: your session IAM user

    - Define key usage permissions: your session IAM user

    - Review and select **Finish**

1. Create a DynamoDB table. This table will be used to store the user's encrypted password.

    DynamoDB table parameters:

    - Table name: `demo-kms`

    - Partition key: `appuser`

    - Leave defaults and select **Create table**

1. 