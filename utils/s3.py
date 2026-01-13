import boto3
import os
import uuid

s3 = boto3.client("s3")
BUCKET = os.environ["S3_BUCKET"]

def upload(local_path, folder):
    key = f"{folder}/{uuid.uuid4()}{os.path.splitext(local_path)[1]}"
    s3.upload_file(local_path, BUCKET, key)
    return f"s3://{BUCKET}/{key}"

def download(s3_path, local_path):
    _, _, bucket_key = s3_path.partition("s3://")
    bucket, _, key = bucket_key.partition("/")
    s3.download_file(bucket, key, local_path)
