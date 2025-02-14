from flask import jsonify
import boto3

def fetch_s3_buckets():
    try:
        s3_client = boto3.client("s3")
        response = s3_client.list_buckets()
        filtered_buckets = []

        for bucket in response["Buckets"]:
            bucket_name = bucket["Name"]
            try:
                tag_response = s3_client.get_bucket_tagging(Bucket=bucket_name)
                tags = {tag["Key"]: tag["Value"] for tag in tag_response["TagSet"]}

                required_tags = {"Owner": "guytamari"}

                if all(tags.get(key) == value for key, value in required_tags.items()):
                    location = s3_client.get_bucket_location(Bucket=bucket_name).get("LocationConstraint", "us-east-1")
                    filtered_buckets.append({
                        "name": bucket_name,
                        "region": location,
                        "tags": tags
                    })

            except s3_client.exceptions.ClientError as e:
                if "NoSuchTagSet" in str(e):
                    print(f"No tags found for {bucket_name}")
                else:
                    print(f"Error fetching tags for {bucket_name}: {e}")

        return jsonify({"buckets": filtered_buckets}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
