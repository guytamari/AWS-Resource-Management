from flask import jsonify
import boto3
import json
import os

BUCKETS_FILE = "s3_buckets.json"

def load_bucket_names():
    if os.path.exists(BUCKETS_FILE):
        with open(BUCKETS_FILE, "r") as f:
            return json.load(f)
    return []

def fetch_s3_buckets():
    try:
        s3_client = boto3.client("s3")
        stored_buckets = load_bucket_names()
        filtered_buckets = []

        for bucket_name in stored_buckets:
            try:
                # Check if bucket exists
                s3_client.head_bucket(Bucket=bucket_name)

                url = f"https://{bucket_name}.s3.us-east-1.amazonaws.com"

                filtered_buckets.append({
                    "name": bucket_name,
                    "url": url
                })

            except s3_client.exceptions.ClientError:
                print(f"Bucket {bucket_name} no longer exists, removing from list.")
                stored_buckets.remove(bucket_name)
                with open(BUCKETS_FILE, "w") as f:
                    json.dump(stored_buckets, f)

        return jsonify({"buckets": filtered_buckets}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
