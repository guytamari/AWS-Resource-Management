import boto3
import os
import json
from .config import get_s3_config
from flask import jsonify

BUCKETS_FILE = "s3_buckets.json"


def upload_files_to_s3(temp_files):
    BUCKET_NAME, _ = get_s3_config()
    s3_client = boto3.client("s3")
    for file_path in temp_files:
        file_name = os.path.basename(file_path)
        s3_client.upload_file(file_path, BUCKET_NAME, file_name)
        print(f"uploaded {file_name} to {BUCKET_NAME}")



def save_bucket_name(bucket_name):
    try:
        if os.path.exists(BUCKETS_FILE):
            with open(BUCKETS_FILE, "r") as f:
                buckets = json.load(f)
        else:
            buckets = []

        if bucket_name not in buckets:
            buckets.append(bucket_name)
            with open(BUCKETS_FILE, "w") as f:
                json.dump(buckets, f)

    except Exception as e:
        print(f"error saving bucket name: {e}")

def create_s3():
    BUCKET_NAME, ACCESS_TYPE = get_s3_config()
    s3_client = boto3.client("s3")

    response = s3_client.create_bucket(Bucket=BUCKET_NAME)

    tags = [
        {"Key": "Name", "Value": "guytamari-bucket"},
        {"Key": "Owner", "Value": "guytamari"},
        {"Key": "CreatedBy", "Value": "boto3"}
    ]
    s3_client.put_bucket_tagging(Bucket=BUCKET_NAME, Tagging={"TagSet": tags})

    if ACCESS_TYPE == 'public':
        s3_client.put_public_access_block(
            Bucket=BUCKET_NAME,
            PublicAccessBlockConfiguration={
                "BlockPublicAcls": False,
                "IgnorePublicAcls": False,
                "BlockPublicPolicy": False,
                "RestrictPublicBuckets": False
            }
        )
        public_policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "PublicReadGetObject",
                    "Effect": "Allow",
                    "Principal": "*",
                    "Action": "s3:GetObject",
                    "Resource": f"arn:aws:s3:::{BUCKET_NAME}/*"
                }
            ]
        }
        s3_client.put_bucket_policy(Bucket=BUCKET_NAME, Policy=json.dumps(public_policy))


    save_bucket_name(BUCKET_NAME)

    return jsonify({
        "name": BUCKET_NAME,
        "url": f"https://{BUCKET_NAME}.s3.us-east-1.amazonaws.com",
        "tags": {tag["Key"]: tag["Value"] for tag in tags}
    }), 201
