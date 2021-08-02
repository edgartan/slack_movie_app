from datetime import datetime
import boto3
from botocore.exceptions import ClientError


def convert_date(date: str) -> str:
    dt = datetime.strptime(date, "%Y-%m-%d")
    dt = dt.strftime("%b %d, %Y")
    return dt


def create_message_blocks(title: str, date: str, overview: str, poster_url: str) -> list:
    movie_message = [
        {
            "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "Here's is the movie info you requested!"
                    }
        },
        {
            "type": "header",
                    "text": {
                        "type": "plain_text",
                        "text": title
                    }
        },
        {
            "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Release date:* " + convert_date(date) + " \n" + overview
                    },
            "accessory": {
                        "type": "image",
                        "image_url": poster_url,
                        "alt_text": "movie poster"
                    }
        }
    ]
    return movie_message


def get_secret(key_name):

    secret_name = "dev/slackmovieapp"
    region_name = "us-east-2"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
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
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response[key_name]
    return secret
