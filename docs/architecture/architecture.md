# UptimeHub Architecture

## Overview

UptimeHub is a cloud-native monitoring application deployed to Microsoft Azure.

The platform monitors configured HTTP endpoints, records their status and
response time, and exposes operational metrics for monitoring and alerting.

## High-Level Architecture

Users
  |
  v
Azure Application Gateway
  |
  v
AKS Ingress
  |
  v
Backend API
  |
  +--------------------+
  |                    |
  v                    v
PostgreSQL          Azure Managed Redis
  ^                    |
  |                    |
  +--------+-----------+
           |
       Scheduler
           |
         Redis
           |
        Workers
           |
           v
   External Websites

Observability:

Backend / Scheduler / Workers
           |
           v
       Prometheus
           |
           v
        Grafana

Prometheus
    |
    v
Alertmanager
    |
    v
Email Alerts

## Azure Infrastructure

The development environment is deployed in Azure Poland Central.

Core Azure services include:

- Azure Kubernetes Service (AKS)
- Azure Container Registry (ACR)
- Azure Database for PostgreSQL Flexible Server
- Azure Managed Redis
- Azure Key Vault
- Azure Application Gateway
- Azure Virtual Network
- Private Endpoints and Private DNS
- Azure Monitor and Log Analytics

## Networking

UptimeHub uses the VNet:

`vnet-uptimehub-dev`

Address space:

`10.10.0.0/16`

Subnets:

- AKS: `10.10.0.0/20`
- Application Gateway: `10.10.16.0/24`
- Private Endpoints: `10.10.17.0/24`
- PostgreSQL: `10.10.18.0/24`

PostgreSQL and Redis use private connectivity.

Azure Application Gateway provides the public application entry point.

## Kubernetes Architecture

Application workloads run in the namespace:

`uptimehub-dev`

Main workloads:

- uptimehub-backend
- uptimehub-scheduler
- uptimehub-worker
- uptimehub-db-migration

The backend and workers use multiple replicas for availability.

Horizontal Pod Autoscalers provide scaling capability.

PodDisruptionBudgets protect application availability during voluntary
disruptions.

## Application Components

### Backend

FastAPI REST API responsible for monitor management and manual checks.

### Scheduler

Finds active monitors that are due for execution and places monitoring jobs
onto Redis.

### Worker

Consumes jobs from Redis, performs HTTP checks, and stores results in
PostgreSQL.

### PostgreSQL

Stores monitor configuration and monitoring results.

### Redis

Provides the monitoring job queue and duplicate-job protection.

## CI/CD

Application flow:

GitHub
  |
  v
Azure DevOps
  |
  v
Tests and Security Scanning
  |
  v
Docker Build
  |
  v
Azure Container Registry
  |
  v
AKS

Infrastructure flow:

Terraform Validate
  |
  v
Security Scan
  |
  v
Terraform Plan
  |
  v
Approval
  |
  v
Terraform Apply

## Secrets

Application secrets are stored in Azure Key Vault.

AKS workloads access Key Vault using Azure Workload Identity and the
Secrets Store CSI Driver.

Secrets are not stored in Git.
