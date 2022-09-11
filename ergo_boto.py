import json
import logging
import boto3
from botocore.config import Config
from botocore.exceptions import ClientError
import requests
from uuid import uuid4


def create_presigned_url(data_bucket_name, metadata_bucket_name, object_name, expiration=3600):
    s3_client = boto3.client('s3', config=Config(signature_version='s3v4'),)

    request_id = str(uuid4())
    s3_filename = f"{request_id}-{object_name}"

    try:
        response = s3_client.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': data_bucket_name,
                'Key': s3_filename,
                'ContentType': 'application/octet-stream'
            },
            ExpiresIn=expiration
        )

        metadata = {'usecase': 'OMB', 'type': 'PDF', 'region': 'Bayern'}
        save_request_metadata_to_s3(request_id, metadata_bucket_name, metadata)

    except ClientError as e:
        logging.error(e)
        return None
    return response


def save_request_metadata_to_s3(request_id, bucket_name, metadata):
    s3_client = boto3.client(
        's3',
        config=Config(signature_version='s3v4'),
    )

    output = {'request_id': request_id, **metadata}

    response = s3_client.put_object(
        Body=json.dumps(output),
        Bucket=bucket_name,
        Key=request_id
    )
    print(response['ResponseMetadata'])
    print(response['ETag'])
    return response


upload_filename = 'file.pdf'

response_url = create_presigned_url(
    data_bucket_name="luq89",
    metadata_bucket_name="luq89-metadata",
    object_name=upload_filename,
    expiration=3600
)

print(response_url)

file_to_upload = "/Users/luq89/PycharmProjects/argocd_test/file.pdf"
# headers = {'content-type': 'application/octet-stream', 'abc':'def'}
headers = {'Content-Type': 'application/octet-stream'}
# headers = {}
response_for_put = requests.put(response_url, data=file_to_upload, headers=headers)
print(f"response_for_put = {response_for_put}")
print(f"response_for_put.request = {response_for_put.request}")
print(f"response_for_put.request.headers = {response_for_put.request.headers}")
print(f"response_for_put.request.body = {response_for_put.request.body}")
print(f"response_for_put headers = {response_for_put.headers}")
print(f"response_for_put request headers = {response_for_put.request.headers}")
# print(f"response_for_put request headers = {response_for_put.request}")
exit(0)



