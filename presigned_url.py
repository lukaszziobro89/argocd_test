from botocore.config import Config
from botocore.exceptions import ClientError
from uuid import uuid4
import boto3
import json
import logging
import requests


class S3PresignedUrlGenerator:

    def __init__(self, data_bucket_name, metadata_bucket_name, object_name, expiration=3600):
        self.s3_client = boto3.client('s3', config=Config(signature_version='s3v4'))
        self.data_bucket_name = data_bucket_name
        self.metadata_bucket_name = metadata_bucket_name
        self.object_name = object_name
        self.expiration = expiration

    def create_presigned_url(self):
        request_id = str(uuid4())
        s3_filename = f"{request_id}-{self.object_name}"

        try:
            response = self.s3_client.generate_presigned_url(
                ClientMethod='put_object',
                Params={
                    'Bucket': self.data_bucket_name,
                    'Key': s3_filename,
                    'ContentType': 'application/octet-stream'
                },
                ExpiresIn=self.expiration
            )

            metadata = {'usecase': 'OMB', 'type': 'PDF', 'region': 'Bayern'}
            self.save_request_metadata_to_s3(request_id, metadata)

        except ClientError as e:
            logging.error(e)
            return None
        return response

    def save_request_metadata_to_s3(self, request_id, metadata):
        output = {'request_id': request_id, **metadata}

        response = self.s3_client.put_object(
            Body=json.dumps(output),
            Bucket=self.metadata_bucket_name,
            Key=request_id
        )
        print(response['ResponseMetadata'])
        print(response['ETag'])
        return response


request = S3PresignedUrlGenerator("luq89", "luq89-metadata", 'file.pdf')
response_url = request.create_presigned_url()
print(response_url)

# exit(0)
# headers = {'content-type': 'application/octet-stream', 'abc':'def'}
headers = {'Content-Type': 'application/octet-stream'}
# headers = {}

file_to_upload = 'file.pdf'
response_for_put = requests.put(response_url, data=file_to_upload, headers=headers)

# print(f"response_for_put = {response_for_put}")
# print(f"response_for_put.request = {response_for_put.request}")
# print(f"response_for_put.request.headers = {response_for_put.request.headers}")
# print(f"response_for_put.request.body = {response_for_put.request.body}")
# print(f"response_for_put headers = {response_for_put.headers}")
# print(f"response_for_put request headers = {response_for_put.request.headers}")
# print(f"response_for_put request headers = {response_for_put.request}")
# exit(0)



