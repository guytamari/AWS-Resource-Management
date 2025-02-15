import boto3
import json
import os
HOSTEDZONE_FILE = "hostedzone.json"

def save_hosted_zone_to_file(hosted_zone_data):
    if os.path.exists(HOSTEDZONE_FILE):
        try:
            with open(HOSTEDZONE_FILE, "r") as file:
                # Check if the file is empty
                if file.read(1):
                    file.seek(0)  # Move back to the start of the file
                    hosted_zones = json.load(file)
                else:
                    hosted_zones = []  # Handle empty file as an empty list
        except json.JSONDecodeError:
            # If the file exists but contains invalid JSON, handle the error
            print(f"Error: {HOSTEDZONE_FILE} contains invalid JSON.")
            hosted_zones = []
    else:
        hosted_zones = []

    hosted_zones.append(hosted_zone_data)

    with open(HOSTEDZONE_FILE, "w") as file:
        json.dump(hosted_zones, file, indent=4)

def create_hostedzone(domain_name, description, access_type, tag_name):
    REGION = "us-east-1"
    GUYTAMARI_VPC_ID = "vpc-004a75684f5853e1a"
    client = boto3.client("route53")
    access_type = access_type.lower()
    PrivateZone = True
    match access_type:
        case "private":
            PrivateZone = True
        case _:
            PrivateZone = False
    
    response_dict = {
        "Name": domain_name,
        "CallerReference": str(hash(domain_name)),
        "HostedZoneConfig": {
            "Comment": description,
            "PrivateZone": PrivateZone
        }
    }
    if PrivateZone:
        response_dict["VPC"] = {"VPCRegion": REGION,"VPCId": GUYTAMARI_VPC_ID}
    
    
    response = client.create_hosted_zone(**response_dict)
    hosted_zone_id = response["HostedZone"]["Id"].split("/")[-1]
    
    client.change_tags_for_resource(
        ResourceType="hostedzone",
        ResourceId=hosted_zone_id,
        AddTags=[{"Key": "Name", "Value": tag_name}]    
    )

    
    hosted_zone_data = {
        "domain_name": domain_name,
        "hosted_zone_id": hosted_zone_id,
        "description": description,
        "access_type": access_type,
        "tag_name": tag_name
    }

    save_hosted_zone_to_file(hosted_zone_data)
    print(f"Hosted zone {domain_name} created successfully with ID: {hosted_zone_id}")
    return hosted_zone_id