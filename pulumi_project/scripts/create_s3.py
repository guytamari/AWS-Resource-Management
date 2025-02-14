import pulumi
import pulumi_aws as aws
import os
from scripts.config import BUCKET_NAME,ACCESS_TYPE



def create_s3():
    if ACCESS_TYPE == "public":
        acl = "public-read"
    else:
        acl = "private"

    bucket = aws.s3.BucketV2(
        BUCKET_NAME,
        bucket=BUCKET_NAME,
        acl=acl,
        tags={"Name": BUCKET_NAME, "Owner": "guytamari"}
    )
    return bucket

s3 = create_s3()