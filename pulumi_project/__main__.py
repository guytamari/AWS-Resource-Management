import pulumi
import json
import os

stack_name = os.getenv("PULUMI_STACK", "default")
print(stack_name)

# ec2 creation and manage
# ----------------------------------------------
if stack_name == "dev":
    from scripts.create_ec2 import instances
    def get_instance_data(instance):
        return {
            "id": instance.id.apply(lambda x: x),
            "public_ip": instance.public_ip.apply(lambda x: x),
            "instance_type": instance.instance_type
        }

    instance_data = [get_instance_data(instance) for instance in instances]

    def save_instance_data_to_file(instances_data):
        with open("ec2_instances.json", "w") as f:
            json.dump(instances_data, f)

    pulumi.Output.all(instance_data).apply(save_instance_data_to_file)

    pulumi.export("instance_ids", [instance.id for instance in instances])
    pulumi.export("public_ips", [instance.public_ip for instance in instances])
    # ec2 creation and manage
    # ----------------------------------------------
elif stack_name == "s3":
    from scripts.create_s3 import s3

    # S3 Bucket creation and management
    # pulumi.export("s3_bucket", s3.id)
    # pulumi.export("bucket_name", s3.id)
    # pulumi.export("bucket_url", pulumi.Output.concat("https://", s3.bucket_regional_domain_name))

else:
    raise ValueError(f"Unknown stack: {stack_name}")
