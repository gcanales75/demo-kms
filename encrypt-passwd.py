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

kms = boto3.client('kms', config=my_config)
dynamodb = boto3.resource('dynamodb', config=my_config)
tableName = 'demo-kms'

## Add 'password' argument from the console to the py script as $passwd variable
passwd=sys.argv[1]

## Add 'KMS key' argument from the console to the py script as $kms_key_id variable
kms_key_id=sys.argv[2]

## Create a random user
user = random.choice(range(10001, 99999))

## Encrypt the password with the KMS key created referencing it with its alias
encrypted = kms.encrypt(
    KeyId=kms_key_id,
    Plaintext=passwd,
    EncryptionAlgorithm='SYMMETRIC_DEFAULT'
)
encryptedpasswd = encrypted['CiphertextBlob']

## Put the encypted password as an item in the DynamoDB table just created
table = dynamodb.Table(tableName)
putItem = table.put_item(
    Item={
        'appuser': str(user),
        'userpasswd': encryptedpasswd  
    }
)

print('A new encrypted password for user:', user, 'has been stored in DynamoDB')
