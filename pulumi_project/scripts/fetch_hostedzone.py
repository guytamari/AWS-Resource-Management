import json
import os

HOSTEDZONE_FILE = "hostedzone.json"

def fetch_hostedzone():
    if os.path.exists(HOSTEDZONE_FILE):
        with open(HOSTEDZONE_FILE, "r") as file:
            hosted_zones = json.load(file)
    else:
        hosted_zones = []

    return {"hosted_zones": hosted_zones}, 200

