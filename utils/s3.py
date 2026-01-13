import os

try:
    import boto3
    S3_ENABLED = "S3_BUCKET" in os.environ
except ImportError:
    boto3 = None
    S3_ENABLED = False

BUCKET = os.environ.get("S3_BUCKET")

if S3_ENABLED:
    s3 = boto3.client("s3")
else:
    s3 = None


def upload_dir(local_dir, s3_prefix):
    if not S3_ENABLED:
        print("⚠️ S3 upload skipped (S3_BUCKET not set)")
        return

    for root, _, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            s3_key = os.path.join(
                s3_prefix,
                os.path.relpath(local_path, local_dir)
            )
            s3.upload_file(local_path, BUCKET, s3_key)


def download_dir(s3_prefix, local_dir):
    if not S3_ENABLED:
        print("⚠️ S3 download skipped (S3_BUCKET not set)")
        return

    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=BUCKET, Prefix=s3_prefix):
        for obj in page.get("Contents", []):
            local_path = os.path.join(
                local_dir,
                os.path.relpath(obj["Key"], s3_prefix)
            )
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            s3.download_file(BUCKET, obj["Key"], local_path)
