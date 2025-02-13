import pulumi
import pulumi_aws as aws
import os
from scripts.config import BUCKET_NAME,ACCESS_TYPE



def create_s3():
    if ACCESS_TYPE == "public":
        acl = "public-read"
    else:
        acl = "private"

    # bucket = aws.s3.BucketV2(BUCKET_NAME,
    #     acl=acl,
    # )
    # if acl == 'public-read':
    #     bucket_policy = aws.s3.BucketPolicy('my-bucket-policy',
    #         bucket=bucket.id,
    #         policy=bucket.id.apply(lambda id: f'''{{
    #             "Version": "2012-10-17",
    #             "Statement": [
    #                 {{
    #                     "Effect": "Allow",
    #                     "Principal": "*",
    #                     "Action": "s3:GetObject",
    #                     "Resource": "arn:aws:s3:::{id}/*"
    #                 }}
    #             ]
    #         }}''')
    #     )
    bucket = aws.s3.BucketV2(
        BUCKET_NAME,
        bucket=BUCKET_NAME,
        acl=acl,
        tags={"Name": BUCKET_NAME, "Owner": "guytamari"}
    )
    return bucket

s3 = create_s3()