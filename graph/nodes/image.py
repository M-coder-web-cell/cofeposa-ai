import os
from utils.s3 import BUCKET, s3, S3_ENABLED

# The pipeline expects `state["image_path"]` to be either a local path
# or an `s3://...` URI. Instead of generating an image locally, the
# pipeline will select an image from the project's S3 bucket under
# the `images/` prefix. You may provide an explicit key via the
# `IMAGE_S3_KEY` environment variable (e.g. `images/example.png`).

def image_node(state):
    # If caller provided an explicit S3 key, use that.
    image_key = os.environ.get("IMAGE_S3_KEY")
    if image_key:
        image_key = image_key.lstrip("/")
        state["image_path"] = f"s3://{BUCKET}/{image_key}"
        return state

    # Otherwise list objects under the `images/` prefix and pick the first file.
    if not S3_ENABLED or s3 is None:
        raise RuntimeError("S3 is not enabled; set S3_BUCKET and ensure boto3 is available")

    paginator = s3.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=BUCKET, Prefix="images/"):
        for obj in page.get("Contents", []):
            key = obj.get("Key")
            if not key or key.endswith("/"):
                continue
            state["image_path"] = f"s3://{BUCKET}/{key}"
            return state

    raise RuntimeError("No image found in S3 under the 'images/' prefix")