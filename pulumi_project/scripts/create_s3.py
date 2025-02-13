import pulumi
import pulumi_aws as aws
import os
from scripts.config import BUCKET_NAME,ACCESS_TYPE


if ACCESS_TYPE == "PUBLIC":
    acl = aws.s3.CannedAcl.PUBLIC_READ
else:
    acl = aws.s3.CannedAcl.PRIVATE

def create_s3():
    bucket = aws.s3.Bucket(
        "guytamari-bucket",
        bucket=BUCKET_NAME,
        acl=acl,
        tags={"Name": BUCKET_NAME, "Owner": "guytamari"}
    )
    return s3
