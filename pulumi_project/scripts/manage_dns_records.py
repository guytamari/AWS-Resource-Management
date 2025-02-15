import boto3

route53_client = boto3.client("route53")





def fetch_dns_records(hosted_zone_id):
    response = route53_client.list_resource_record_sets(HostedZoneId=hosted_zone_id)
    records = response.get("ResourceRecordSets", [])
    return records


def add_dns_record(hosted_zone_id, record_name, record_type, record_value):

    response = route53_client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            "Changes": [
                {
                    "Action": "CREATE",
                    "ResourceRecordSet": {
                        "Name": record_name,
                        "Type": record_type,
                        "TTL": 300,
                        "ResourceRecords": [{"Value": record_value}],
                    },
                }
            ]
        },
    )
    return response["ChangeInfo"]["Status"] == "PENDING"



def delete_dns_record(hosted_zone_id, record_name, record_type):
    response = route53_client.change_resource_record_sets(
        HostedZoneId=hosted_zone_id,
        ChangeBatch={
            "Changes": [
                {
                    "Action": "DELETE",
                    "ResourceRecordSet": {
                        "Name": record_name,
                        "Type": record_type,
                        "TTL": 300,
                        "ResourceRecords": [{"Value": "dummy"}],
                    },
                }
            ]
        },
    )
    return response["ChangeInfo"]["Status"] == "PENDING"

