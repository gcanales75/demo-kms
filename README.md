# Security Best Practices - KMS Demo

In this demo you will demonstrate how to perform client-side encrypt/decript operations on *strings* using `AWS SDK` in a very simple scenario and running a couple of python (boto3) scripts.

*Diagram:*

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

1. Open **CloudShell**

1. Download encrypt and decrypt python script files

    ```sh
    curl -o decrypt-passwd.py https://raw.githubusercontent.com/gcanales75/demo-kms/main/decrypt-passwd.py
    curl -o encrypt-passwd.py https://raw.githubusercontent.com/gcanales75/demo-kms/main/encrypt-passwd.py
    ```

1. To encrypt a password *string* run the below command:

    ```sh
    python3 encrypt-passwd.py mySuperSecretPasswd
    ```

    You could replace `mySuperSecretPasswd` with a different password string

    You must see a similar output:

    ```sh
    -->> Encrypting your very secret password
    A new encrypted password for user: xxxxx has been stored in DynamoDB
    ```

1. Go to DynamoDB and explore the items in table `demo-kms`. You must see an item with the user number similar to the CloudShell stdout. You will also notice the `userpasswd` value is the encrypted.

1. You now will retrieve the unscrypted password from the DynamosDB table running a second python script which references the `user` number. Run the below command replacing the `user` placeholder with the actual `user` number displayed after the encryption file run.

    ```sh
    python3 decrypt-passwd.py xxxxx
    ```

    You must see a similar output:

    ```sh
    -->> Decrypting the very secret password for user: xxxxx
    Is this your decrypted password? -> mySuperSecretPasswd
    ```

### Highlights

1. Customers could protect sensitive information such as PII or financial records, prior to being transmited to a storage service over a network (client-side encryption) using KMS encryption keys.