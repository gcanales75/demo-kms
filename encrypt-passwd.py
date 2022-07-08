import boto3
import random
import os
import json
from botocore.config import Config
import sys

print('-->> Encrypting your very secret password')

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
dynamodb = boto3.resource('dynamodb', config=my_config)
## Set DynamoDB table name variable
tableName = 'demo-kms'
## Pass 'password' argument from the console to the py script
passwd=sys.argv[1]
## Create a random user
user = random.choice(range(10001, 99999))
## Encrypt the password with the KMS key created referencing it with its alias
encrypted = kms.encrypt(
    KeyId='alias/demo-kms',
    Plaintext=passwd,
    EncryptionAlgorithm='SYMMETRIC_DEFAULT'
)
encryptedpasswd = encrypted['CiphertextBlob']
## Put the encypted password as an item in the DynamoDB table just created
table = dynamodb.Table(tableName)
putItem = table.put_item(
    Item={                                  ## <-- Encrypted password key/value
        'appuser': str(user),
        'userpasswd': encryptedpasswd  
    }
)

print('A new encrypted password for user:', user, 'has been stored in DynamoDB')
