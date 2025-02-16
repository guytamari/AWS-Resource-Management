import boto3
import json
from flask import request, jsonify

route53_client = boto3.client("route53")
HOSTED_ZONE_FILE = "hostedzone.json"

def delete_hosted_zone():
    try:
        data = request.json
        hosted_zone_id = data.get("hosted_zone_id")

        # get all the current hostedzone from json file
        with open(HOSTED_ZONE_FILE, "r") as f:
            hosted_zones = json.load(f)

        # get all record set
        record_sets = route53_client.list_resource_record_sets(HostedZoneId=hosted_zone_id)

        changes = []
        for record in record_sets["ResourceRecordSets"]:
            if record["Type"] not in ["NS", "SOA"]:  # Keep NS and SOA records
                changes.append({
                    "Action": "DELETE",
                    "ResourceRecordSet": record
                })

        if changes:
            route53_client.change_resource_record_sets(
                HostedZoneId=hosted_zone_id,
                ChangeBatch={"Changes": changes}
            )

        # delete the hostedzone
        response = route53_client.delete_hosted_zone(Id=hosted_zone_id)

        # upadte the hostedzone.json
        updated_zones = [zone for zone in hosted_zones if zone["hosted_zone_id"] != hosted_zone_id]

        with open(HOSTED_ZONE_FILE, "w") as f:
            json.dump(updated_zones, f, indent=4)

        return jsonify({"status": "success", "message": "Hosted zone deleted", "response": response}), 200

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500
