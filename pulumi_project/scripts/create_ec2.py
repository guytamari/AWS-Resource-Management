import pulumi
import pulumi_aws as aws
import os
from scripts.config import INSTANCE_TYPE, AMI_ID, TAG_NAME, NUM_INSTANCES

def create_ec2_instances():
    instances = []
    for i in range(NUM_INSTANCES):
        instance = aws.ec2.Instance(
            f"guytamari-instance-{i+1}",
            instance_type=INSTANCE_TYPE,
            ami=AMI_ID,
            tags={"Name": f"{TAG_NAME}-{i+1}", "Owner": "guytamari"}
        )
        instances.append(instance)

    return instances

instances = create_ec2_instances()
