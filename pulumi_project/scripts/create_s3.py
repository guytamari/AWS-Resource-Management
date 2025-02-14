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
    
    
    s3_client.put_public_access_block(
        Bucket=BUCKET_NAME,
        PublicAccessBlockConfiguration={
            "BlockPublicAcls": False,
            "IgnorePublicAcls": False,
            "BlockPublicPolicy": False,
            "RestrictPublicBuckets": False
        }
    )
    
    
    
    
    if ACCESS_TYPE == 'public':
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


    return response

s3 = create_s3()



    # Create S3 bucket
    # bucket = aws.s3.Bucket(
    #     BUCKET_NAME,
    #     bucket=BUCKET_NAME,
    #     force_destroy=True,
    #     tags={"Name": BUCKET_NAME, "Owner": "guytamari"}
    # )

    # # Set Object Ownership to "BucketOwnerEnforced"
    # ownership = aws.s3.BucketOwnershipControls("myawsbucketOwnership",
    #     bucket=bucket.id,
    #     rule=aws.s3.BucketOwnershipControlsRuleArgs(
    #         object_ownership="BucketOwnerEnforced"
    #     )
    # )

    # # Set bucket policy for public access
    # if ACCESS_TYPE == "public":
    #     bucket_policy = aws.s3.BucketPolicy("publicBucketPolicy",
    #         bucket=bucket.id,
    #         policy=bucket.id.apply(lambda id: f"""
    #         {{
    #             "Version": "2012-10-17",
    #             "Statement": [
    #                 {{
    #                     "Effect": "Allow",
    #                     "Principal": "*",
    #                     "Action": "s3:GetObject",
    #                     "Resource": "arn:aws:s3:::{id}/*"
    #                 }}
    #             ]
    #         }}
    #         """.strip())  # Ensure valid JSON format
    #     )

    # # Disable Block Public Access settings if public
    # public_access_block = aws.s3.BucketPublicAccessBlock("publicAccessBlock",
    #     bucket=bucket.id,
    #     block_public_acls=False,
    #     block_public_policy=False,
    #     ignore_public_acls=False,
    #     restrict_public_buckets=False
    # ) if ACCESS_TYPE == "public" else None