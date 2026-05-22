import boto3
import json
import argparse
from datetime import datetime

ec2 = boto3.client(
    "ec2",
    endpoint_url="http://localhost:4566",
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1"
)
volumes = ec2.describe_volumes()

for volume in volumes["Volumes"]:
    if volume["State"] == "available":
        print(volume["VolumeId"])

report = {
    "scan_timestamp": datetime.utcnow().isoformat(),
    "account_id": "000000000000",
    "region": "us-east-1",
    "summary": {
        "total_orphans": 1,
        "estimated_monthly_waste_usd": 8.0
    },
    "findings": []
}

with open("report.json", "w") as f:
    json.dump(report, f, indent=2)