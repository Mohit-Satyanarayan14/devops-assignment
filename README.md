Project Overview:

This project implements a Cost Janitor system using Terraform, LocalStack, Python, and GitHub Actions.
The pipeline provisions AWS-like resources locally using LocalStack and scans for orphaned resources such as unattached EBS volumes.
The CI/CD pipeline automatically fails in dry-run mode if orphaned resources are detected.

Tech Stack Used:
-TERRAFORM
-LocalStack
-Python
-GitHub Actions
-DOCKER

CHALLENGES FACES + Fixes:

1)LocalStack Container failed to start 
Fix: Pinned the localstack image version to 3.5 instead of the latest image

2)Terraform endpoints connectivity issues
Fix: Configured  terraform provider endpoints correctly for LocalStack

4) Python dependancy conflicts 
Fix: Reduced the requirements.txt to only required dependancies

5) Git push rejected due to large terraform provider files\
Fix: Added .terraform and lock files to .gitignore and removed cached binaries . 

AI tools Used:
Chatgpt : Used for Terraform/Janitor logic and to Debug issues .
