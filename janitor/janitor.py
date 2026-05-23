import boto3
import json
import argparse
import sys

from datetime import datetime, timezone
from constants import *

ec2 = boto3.client(
    "ec2",
    endpoint_url="http://localhost:4566",
    region_name="us-east-1",
    aws_access_key_id="test",
    aws_secret_access_key="test"
)

findings = []


def get_tags(tag_list):
    if not tag_list:
        return {}

    return {tag["Key"]: tag["Value"] for tag in tag_list}


def check_ebs_volumes():
    volumes = ec2.describe_volumes()["Volumes"]

    for volume in volumes:
        if volume["State"] == "available":
            findings.append({
                "resource_id": volume["VolumeId"],
                "resource_type": "ebs_volume",
                "reason": "unattached",
                "age_days": 0,
                "estimated_monthly_cost_usd": (
                    volume["Size"] * EBS_COST_PER_GB
                ),
                "tags": get_tags(volume.get("Tags", [])),
                "suggested_action": "delete",
                "safe_to_auto_delete": True
            })


def check_stopped_instances(days=14):
    reservations = ec2.describe_instances()["Reservations"]

    for reservation in reservations:
        for instance in reservation["Instances"]:

            state = instance["State"]["Name"]

            if state == "stopped":
                findings.append({
                    "resource_id": instance["InstanceId"],
                    "resource_type": "ec2_instance",
                    "reason": f"stopped_more_than_{days}_days",
                    "age_days": days,
                    "estimated_monthly_cost_usd":
                        EC2_T3_MICRO_COST,
                    "tags": get_tags(instance.get("Tags", [])),
                    "suggested_action": "review",
                    "safe_to_auto_delete": False
                })


def check_elastic_ips():
    addresses = ec2.describe_addresses()["Addresses"]

    for address in addresses:
        if "InstanceId" not in address:
            findings.append({
                "resource_id": address["AllocationId"],
                "resource_type": "elastic_ip",
                "reason": "unused_eip",
                "age_days": 0,
                "estimated_monthly_cost_usd":
                    ELASTIC_IP_COST,
                "tags": {},
                "suggested_action": "release",
                "safe_to_auto_delete": True
            })


def check_missing_tags():
    reservations = ec2.describe_instances()["Reservations"]

    for reservation in reservations:
        for instance in reservation["Instances"]:

            tags = get_tags(instance.get("Tags", []))

            missing = []

            for required in REQUIRED_TAGS:
                if required not in tags:
                    missing.append(required)

            if missing:
                findings.append({
                    "resource_id": instance["InstanceId"],
                    "resource_type": "ec2_instance",
                    "reason": f"missing_tags: {missing}",
                    "age_days": 0,
                    "estimated_monthly_cost_usd":
                        EC2_T3_MICRO_COST,
                    "tags": tags,
                    "suggested_action": "tag_resource",
                    "safe_to_auto_delete": False
                })


def generate_report():
    total_cost = sum(
        finding["estimated_monthly_cost_usd"]
        for finding in findings
    )

    report = {
        "scan_timestamp":
            datetime.now(timezone.utc).isoformat(),

        "account_id": "000000000000",

        "region": "us-east-1",

        "summary": {
            "total_orphans": len(findings),
            "estimated_monthly_waste_usd":
                round(total_cost, 2)
        },

        "findings": findings
    }

    with open("report.json", "w") as f:
        json.dump(report, f, indent=2)

    with open("report.md", "w") as f:
        f.write("# Cost Janitor Report\n\n")

        if not findings:
            f.write("No orphaned resources found.\n")
        else:
            for finding in findings:
                f.write(
                    f"- {finding['resource_type']} "
                    f"{finding['resource_id']} "
                    f"-> {finding['reason']}\n"
                )

    return len(findings)


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--dry-run",
        action="store_true"
    )

    parser.add_argument(
        "--delete",
        action="store_true"
    )

    args = parser.parse_args()

    check_ebs_volumes()
    check_stopped_instances()
    check_elastic_ips()
    check_missing_tags()

    total = generate_report()

    print(f"Found {total} orphaned resources")

    if args.dry_run and total > 0:
        print("Dry run detected orphaned resources. No actions will be taken.")


if __name__ == "__main__":
    main()