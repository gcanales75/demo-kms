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

kms = boto3.client('kms', config=my_config)
dynamodb = boto3.client('dynamodb', config=my_config)
tableName = 'demo-kms'

## Pass 'user' argument from the console to the py script
user = sys.argv[1]

## Add 'KMS key' argument from the console to the py script as $kms_key_id variable
kms_key_id=sys.argv[2]

## Get the encrypted password referencing the item partition key (appuser)
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
    KeyId=kms_key_id,
    EncryptionAlgorithm='SYMMETRIC_DEFAULT'
)
decryptedpasswd = decrypted['Plaintext']
decodedpasswd = decryptedpasswd.decode("utf-8")

print('Is this your decrypted password? ->', decodedpasswd)
