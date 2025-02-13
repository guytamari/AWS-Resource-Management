import os

# ----------------------------------------------
# ec2 configirations
INSTANCE_TYPE = os.getenv("INSTANCE_TYPE", "t3.nano")
AMI_CHOICE = os.getenv("AMI", "ubuntu")
TAG_NAME = os.getenv("TAG_NAME", "MyInstance")
NUM_INSTANCES = int(os.getenv("NUM_INSTANCES", "1"))

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

AMI_ID = AMI_IDS.get(AMI_CHOICE, {}).get(INSTANCE_TYPE, "ami-04b4f1a9cf54c11d0")
# ec2 configirations
# ----------------------------------------------

# ----------------------------------------------
# s3 configirations
BUCKET_NAME = os.getenv("BUCKET_NAME","s3-bucket-default")
ACCESS_TYPE = os.getenv("ACCESS_TYPE","PRIVATE").upper()




# s3 configirations
# ----------------------------------------------
