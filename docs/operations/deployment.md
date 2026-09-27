# UptimeHub Deployment Guide

## Application Deployment

Application deployments are performed through Azure DevOps.

Source code is hosted in GitHub.

The application pipeline performs:

1. Backend tests
2. Repository and dependency security scanning
3. Docker image build
4. Push image to Azure Container Registry
5. Container image security scanning
6. Deployment to AKS
7. Smoke test

Each container image uses the Azure DevOps Build ID as its image tag.

## Database Migration

The deployment process runs the Kubernetes Job:

`uptimehub-db-migration`

The Job executes:

`alembic upgrade head`

The pipeline waits for the migration to complete before accepting the
application rollout.

## Kubernetes Deployment

Azure DevOps authenticates to Azure through Workload Identity Federation.

The pipeline obtains AKS credentials, renders the Kubernetes manifests, and
deploys the application.

It waits for successful rollouts of:

- backend
- scheduler
- worker

## Smoke Test

After deployment, Azure DevOps sends an HTTP request through Application
Gateway to:

`/health`

A failed health request causes the deployment pipeline to fail.

## Infrastructure Deployment

Infrastructure is managed through the Terraform pipeline.

The process is:

1. Terraform Validate
2. Terraform security scan
3. Terraform Plan
4. Approval
5. Terraform Apply

The Apply stage uses the plan produced by the Plan stage.

Infrastructure should normally be changed through Terraform rather than
manual Azure Portal modifications.
