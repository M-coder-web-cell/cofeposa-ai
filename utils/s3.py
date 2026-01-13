import os
import boto3
from uuid import uuid4

BUCKET = os.environ["S3_BUCKET_NAME"]

s3 = boto3.client("s3")

def upload(local_path: str, prefix: str) -> str:
    key = f"{prefix}/{uuid4().hex}_{os.path.basename(local_path)}"
    s3.upload_file(local_path, BUCKET, key)
    return f"s3://{BUCKET}/{key}"

def download(s3_uri: str, local_path: str):
    _, _, path = s3_uri.partition("s3://")
    bucket, key = path.split("/", 1)
    s3.download_file(bucket, key, local_path)
