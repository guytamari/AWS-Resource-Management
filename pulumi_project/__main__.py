import pulumi
import pulumi_aws as aws
import os
import json

instance_type = os.getenv("INSTANCE_TYPE", "t3.nano")
ami_choice = os.getenv("AMI", "ubuntu")
tag_name = os.getenv("TAG_NAME", "MyInstance")
num_instances = int(os.getenv("NUM_INSTANCES", "1"))

AMI_IDS = {
    "ubuntu": {
        "t3.nano": "ami-04b4f1a9cf54c11d0",  
        "t4g.nano": "ami-0a7a4e87939439934",  
    },
    "amazon_linux": {
        "t3.nano": "ami-085ad6ae776d8f09c",  
        "t4g.nano": "ami-0e532fbed6ef00604", 
    },
}

ami_id = AMI_IDS.get(ami_choice, {}).get(instance_type, "ami-12345678")

instances = []
for i in range(num_instances):
    instance = aws.ec2.Instance(
        f"guytamari-instance-{i+1}",
        instance_type=instance_type,
        ami=ami_id,
        tags={"Name": f"{tag_name}-{i+1}", "Owner": "guytamari"}
    )
    instances.append(instance)

# Use apply to get the actual values from the Output objects and write them to a file
def get_instance_data(instance):
    return {
        "id": instance.id.apply(lambda x: x),  # Unwrap the Output to get the actual value
        "public_ip": instance.public_ip.apply(lambda x: x),
        "instance_type": instance_type
    }


instance_data = [get_instance_data(instance) for instance in instances]

# Save the instance data to a file once the values are resolved
def save_instance_data_to_file(instances_data):
    with open("ec2_instances.json", "w") as f:
        json.dump(instances_data, f)

# Once Pulumi applies the resources, save the instance data
pulumi.Output.all(instance_data).apply(save_instance_data_to_file)

pulumi.export("instance_ids", [instance.id for instance in instances])
pulumi.export("public_ips", [instance.public_ip for instance in instances])
