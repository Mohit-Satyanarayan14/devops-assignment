# Submission

## Repository
GitHub Repository:
https://github.com/Mohit-Satyanarayan14/devops-assignment.git

## Walkthrough Video
Video URL:
https://drive.google.com/file/d/1hheY8j81oQfIR9Zr_9GUB33WLRzGmDkd/view?usp=drive_link

---

# Project Overview

This project implements a Cost Janitor system using Terraform, LocalStack, Python, and GitHub Actions.

The infrastructure is provisioned locally using Terraform against LocalStack, while the Python-based Janitor scans for orphaned cloud resources and generates JSON and Markdown reports.

The CI/CD pipeline automates provisioning, scanning, and artifact uploads.

---

# Features

- Terraform-based infrastructure provisioning
- Local AWS simulation using LocalStack
- Orphan resource detection
- JSON and Markdown report generation
- GitHub Actions CI/CD pipeline
- Dry-run governance scanning

---

# Decisions & Deviations

## LocalStack Version Pinning
The LocalStack image version was pinned to `3.5` instead of `latest` to avoid CI instability caused by upstream changes.

## Dry-Run Pipeline Behavior
Initially the pipeline exited with a non-zero status code when orphaned resources were detected. For final submission, the workflow was adjusted to complete successfully while still reporting findings.

## Simplified Cost Estimation
Static pricing constants were used instead of live AWS pricing APIs to keep the implementation reproducible and lightweight.

---

# Challenges Faced

1. GitHub Actions YAML indentation issues
2. LocalStack service container startup failures
3. Terraform provider endpoint configuration issues
4. Dependency conflicts in requirements.txt
5. Terraform cache and provider binaries accidentally committed to Git

These issues were resolved incrementally through CI/CD log debugging, provider stabilization, and workflow adjustments.

---

# AI Usage Disclosure

## Tools Used
- ChatGPT for CI/CD debugging, Terraform troubleshooting, and workflow setup guidance.
- GitHub Copilot for small boilerplate suggestions.

## One Incorrect AI Suggestion
An early suggestion used unstable LocalStack latest images and custom health checks, which caused GitHub Actions failures. The issue was identified through workflow logs and fixed by pinning stable versions.

## One Section Written Without AI
The final debugging decisions and incremental CI/CD troubleshooting process were manually validated and adjusted during implementation.