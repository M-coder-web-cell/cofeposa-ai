import boto3
import os

s3 = boto3.client("s3")
BUCKET = os.environ["S3_BUCKET"]

def upload_dir(local_dir, s3_prefix):
    for root, _, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            s3_key = os.path.join(
                s3_prefix,
                os.path.relpath(local_path, local_dir)
            )
            s3.upload_file(local_path, BUCKET, s3_key)

def download_dir(s3_prefix, local_dir):
    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=BUCKET, Prefix=s3_prefix):
        for obj in page.get("Contents", []):
            local_path = os.path.join(
                local_dir,
                os.path.relpath(obj["Key"], s3_prefix)
            )
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            s3.download_file(BUCKET, obj["Key"], local_path)
