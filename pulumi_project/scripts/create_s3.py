import boto3
import os
import json
from .config import BUCKET_NAME,ACCESS_TYPE


def create_s3():
    
    s3_client = boto3.client("s3")
    response = s3_client.create_bucket(
        Bucket=BUCKET_NAME,)
    
    tags = [
        {
            "Key": "Name",
            "Value": "guytamari-bucket"
            
        },
        {
            "Key": "Owner",
            "Value": "guytamari"
            
        },
            {
            "Key": "CreatedBy",
            "Value": "boto3"
            
            }
        
    ]
    s3_client.put_bucket_tagging(
        Bucket=BUCKET_NAME,
        Tagging={"TagSet": tags}
        
    )
    
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
            s3_client.put_bucket_policy(
            Bucket=BUCKET_NAME,
            Policy=json.dumps(public_policy))

    print(BUCKET_NAME,ACCESS_TYPE)
    return response



def upload_files_to_s3(temp_files):
    s3_client = boto3.client("s3")
    
    for file_path in temp_files:
        file_name = os.path.basename(file_path)
        try:
            s3_client.upload_file(file_path, BUCKET_NAME, file_name)
            print(f"Successfully uploaded {file_name} to S3")
        except Exception as e:
            print(f"Error uploading {file_name}: {e}")



s3 = create_s3()
