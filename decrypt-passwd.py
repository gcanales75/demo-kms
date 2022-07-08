import boto3
import random
import os
import json
from botocore.config import Config
import sys

print('-->> Decrypting the very secret password for user:', sys.argv[1])

## Setting KMS SDK configuration variables
my_config = Config(
    region_name = 'us-east-1',
    signature_version = 'v4',
    retries = {
        'max_attempts': 10,
        'mode': 'standard'
    }
)
## Start KMS boto3 client
kms = boto3.client('kms', config=my_config)
## Start DynamoDB boto3 client
dynamodb = boto3.client('dynamodb', config=my_config)
## Set DynamoDB table name variable
tableName = 'demo-kms'
## Pass 'user' argument from the console to the py script
user = sys.argv[1]
## Look for the encrypted password referencing the item 'key' (user)
item = dynamodb.get_item(
    TableName=tableName,
    Key ={
        'appuser': {
                'S': user
        }
    },
    ProjectionExpression='userpasswd',
)
## Parsing the encrypted password from the 'item' response
encryptedpasswd = item['Item']['userpasswd']['B']

## Decrypt stored password
decrypted = kms.decrypt(
    CiphertextBlob=encryptedpasswd,
    KeyId='alias/demo-kms',
    EncryptionAlgorithm='SYMMETRIC_DEFAULT'
)
decryptedpasswd = decrypted['Plaintext']
decodedpasswd = decryptedpasswd.decode("utf-8")

print('Is this your decrypted password? ->', decodedpasswd)
#print(decrypted)
# demo-no-decrypt Policy