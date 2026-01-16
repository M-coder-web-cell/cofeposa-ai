import os
import shutil
from urllib.parse import urlparse

try:
    import boto3
    S3_ENABLED = "S3_BUCKET" in os.environ
except Exception:
    boto3 = None
    S3_ENABLED = False

BUCKET = os.environ.get("S3_BUCKET")

if S3_ENABLED and boto3 is not None:
    s3 = boto3.client("s3")
else:
    s3 = None

# Use /tmp/ for temporary files (works on macOS and Linux)
TMP_DIR = "/tmp/cofeposa"
os.makedirs(TMP_DIR, exist_ok=True)


def upload_dir(local_dir, s3_prefix):
    if not S3_ENABLED:
        print("⚠️ S3 upload skipped (S3_BUCKET not set)")
        return

    for root, _, files in os.walk(local_dir):
        for file in files:
            local_path = os.path.join(root, file)
            rel = os.path.relpath(local_path, local_dir)
            s3_key = os.path.join(s3_prefix, rel)
            s3.upload_file(local_path, BUCKET, s3_key)


def download_dir(s3_prefix, local_dir):
    if not S3_ENABLED:
        print("⚠️ S3 download skipped (S3_BUCKET not set)")
        return

    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=BUCKET, Prefix=s3_prefix):
        for obj in page.get("Contents", []):
            local_path = os.path.join(local_dir, os.path.relpath(obj["Key"], s3_prefix))
            os.makedirs(os.path.dirname(local_path), exist_ok=True)
            s3.download_file(BUCKET, obj["Key"], local_path)


def upload(local_path, s3_prefix):
    """Upload a single file. Returns S3 URI when uploaded, else local path."""
    if not os.path.exists(local_path):
        raise FileNotFoundError(f"Local file not found: {local_path}")

    if not S3_ENABLED:
        print("⚠️ S3 upload skipped (S3_BUCKET not set)")
        return local_path

    s3_key = os.path.join(s3_prefix, os.path.basename(local_path))
    s3.upload_file(local_path, BUCKET, s3_key)
    return f"s3://{BUCKET}/{s3_key}"


def download(s3_uri_or_local, local_path):
    """Download from s3://... to local path, or copy local file if given a local path."""
    # If it already looks like a local path, just copy or do nothing
    if s3_uri_or_local is None:
        raise ValueError("No source path provided to download()")

    # Handle file:// URIs and local paths FIRST, before S3
    if not s3_uri_or_local.startswith("s3://"):
        parsed = urlparse(s3_uri_or_local)

        # Extract source path: use parsed path for file:// URIs, or original string for local paths
        if parsed.scheme == "file":
            src = parsed.path
        else:
            # Plain local path (no scheme)
            src = s3_uri_or_local

        # Validate source file exists
        if not os.path.exists(src):
            raise FileNotFoundError(f"Local source file not found: {src}")

        # Copy to destination
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        shutil.copyfile(src, local_path)
        return local_path

    # Otherwise assume s3://bucket/key
    if not S3_ENABLED:
        raise RuntimeError("S3 is not enabled (S3_BUCKET not set), cannot download s3:// URI")

    parsed = urlparse(s3_uri_or_local)
    # parsed.netloc is bucket, path is /key
    bucket = parsed.netloc or BUCKET
    key = parsed.path.lstrip("/")
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    s3.download_file(bucket, key, local_path)
    return local_path


def upload_fileobj(fileobj, s3_key, bucket=None):
    """
    Upload a file-like object directly to S3 (no local disk).
    Used for streaming downloads (HF → S3).
    """
    if not S3_ENABLED:
        raise RuntimeError("S3 upload skipped (S3_BUCKET not set)")

    bucket = bucket or BUCKET

    s3.upload_fileobj(
        Fileobj=fileobj,
        Bucket=bucket,
        Key=s3_key
    )

    return f"s3://{bucket}/{s3_key}"
