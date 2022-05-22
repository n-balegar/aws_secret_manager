import boto3
import base64
from botocore.exceptions import ClientError


def get_secret(sn, rn, ss, gc):
    secret_name = sn
    region_name = rn
    
    print("inside calling function")

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(service_name=ss,region_name=region_name)
    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    
    except ClientError as e:
        if e.response['Error']['Code'] == 'DecryptionFailureException':
            # Secrets Manager can't decrypt the protected secret text using the provided KMS key.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InternalServiceErrorException':
            # An error occurred on the server side.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidParameterException':
            # You provided an invalid value for a parameter.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'InvalidRequestException':
            # You provided a parameter value that is not valid for the current state of the resource.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
        elif e.response['Error']['Code'] == 'ResourceNotFoundException':
            # We can't find the resource that you asked for.
            # Deal with the exception here, and/or rethrow at your discretion.
            raise e
            
    if 'SecretString' in get_secret_value_response:
        secret = get_secret_value_response['SecretString']
        print(secret)
        return secret
    else:
        decoded_binary_secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        return decoded_binary_secret
    # return keyName,secretKeyId

    # Your code goes here.
