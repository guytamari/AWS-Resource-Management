import json
import os

HOSTEDZONE_FILE = "hostedzone.json"

def fetch_hostedzone():
    if os.path.exists(HOSTEDZONE_FILE) and os.path.getsize(HOSTEDZONE_FILE) > 0:
        with open(HOSTEDZONE_FILE, "r") as file:
            hosted_zones = json.load(file)
    else:
        hosted_zones = []

    return {"hosted_zones": hosted_zones}, 200

def get_hostzoned_name(hosted_zone_id):
    hostname = ""
    if os.path.exists(HOSTEDZONE_FILE) and os.path.getsize(HOSTEDZONE_FILE) > 0:
        with open(HOSTEDZONE_FILE, "r") as file:
            hosted_zones = json.load(file)
            for zone in hosted_zones:
                if zone.get("hosted_zone_id") == hosted_zone_id:
                    hostname = zone.get("domain_name", "")
                    break

    return hostname