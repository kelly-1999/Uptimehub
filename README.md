# UptimeHub

UptimeHub is a cloud-native uptime monitoring platform deployed on Microsoft Azure.

It monitors HTTP endpoints, records availability and response times, processes monitoring jobs asynchronously, exposes operational metrics, and sends alerts when problems occur.

The project demonstrates a production-style DevOps architecture using Azure, Kubernetes, Terraform, Docker, CI/CD, observability, security scanning, and workload identity.

---

## Architecture

```text
                         Internet
                            |
                            v
                 Azure Application Gateway
                            |
                            v
                      AKS Ingress
                            |
                            v
                     FastAPI Backend
                      /           \
                     /             \
                    v               v
             PostgreSQL       Azure Managed Redis
                                   |
                                   v
                              Job Queue
                             /         \
                            v           v
                      Scheduler      Workers
                                        |
                                        v
                               External HTTP Targets


                    Observability
                         |
        +----------------+----------------+
        |                                 |
        v                                 v
   Prometheus                         Azure Monitor
        |
        +----------+
        |          |
        v          v
     Grafana   Alertmanager
                   |
                   v
              Email Alerts
```

---

## Technology Stack

### Application

- Python
- FastAPI
- SQLAlchemy
- Alembic
- PostgreSQL
- Redis
- Pytest

### Containers and Kubernetes

- Docker
- Azure Kubernetes Service (AKS)
- Kubernetes Deployments
- Services
- Ingress
- ConfigMaps
- Secrets Store CSI Driver
- ServiceAccounts
- NetworkPolicies
- Horizontal Pod Autoscaler
- PodDisruptionBudget
- Kustomize

### Azure

- Azure Kubernetes Service
- Azure Container Registry
- Azure Database for PostgreSQL Flexible Server
- Azure Managed Redis
- Azure Key Vault
- Azure Application Gateway
- Azure Virtual Network
- Private Endpoints
- Private DNS
- Azure Monitor
- Log Analytics
- Managed Identities
- Workload Identity

### Infrastructure and CI/CD

- Terraform
- Azure DevOps Pipelines
- GitHub
- Workload Identity Federation
- Trivy

### Observability

- Prometheus
- Grafana
- Alertmanager
- Azure Monitor
- Log Analytics

---

## Application Components

### Backend API

The backend is a FastAPI application responsible for managing monitors and performing manual monitor checks.

Main API operations include:

```text
POST   /api/v1/monitors
GET    /api/v1/monitors
GET    /api/v1/monitors/{id}
PUT    /api/v1/monitors/{id}
DELETE /api/v1/monitors/{id}
POST   /api/v1/monitors/{id}/check

GET    /health
GET    /metrics
```

### Scheduler

The scheduler searches PostgreSQL for active monitors that are due for execution.

Due monitor IDs are placed onto the Redis job queue.

### Workers

Workers consume jobs from Redis and perform HTTP checks against configured targets.

Results such as availability, HTTP status, response time, and last check time are stored in PostgreSQL.

Multiple worker replicas can process monitoring jobs concurrently.

### Redis

Redis provides:

- asynchronous monitoring job queue
- duplicate-job protection
- communication between scheduler and workers

### PostgreSQL

PostgreSQL stores persistent application data including monitor configuration and monitoring status information.

Database schema changes are managed using Alembic migrations.

---

## Azure Network Architecture

The development environment runs in Azure Poland Central.

The VNet uses:

```text
10.10.0.0/16
```

Subnet design:

| Subnet | Address Range | Purpose |
|---|---|---|
| AKS | `10.10.0.0/20` | Kubernetes nodes and workloads |
| Application Gateway | `10.10.16.0/24` | Public application entry point |
| Private Endpoints | `10.10.17.0/24` | Private Azure service connectivity |
| PostgreSQL | `10.10.18.0/24` | PostgreSQL Flexible Server |

PostgreSQL and Redis are not exposed directly to the public internet.

Private DNS is used to resolve privately connected Azure services.

---

## Kubernetes

Application workloads run in the namespace:

```text
uptimehub-dev
```

Main workloads include:

```text
uptimehub-backend
uptimehub-scheduler
uptimehub-worker
uptimehub-db-migration
```

The Kubernetes configuration includes:

- multiple backend replicas
- multiple worker replicas
- startup, readiness, and liveness probes
- CPU and memory requests
- CPU and memory limits
- Horizontal Pod Autoscaling
- PodDisruptionBudgets
- NetworkPolicies
- Workload Identity
- Key Vault CSI integration

---

## Secrets Management

Application secrets are stored in Azure Key Vault.

Examples include:

```text
database-url
redis-url
```

AKS workloads authenticate to Azure using Azure Workload Identity.

The Secrets Store CSI Driver retrieves secrets from Key Vault and makes them available to the application.

This avoids storing application secrets directly in Git.

---

## Infrastructure as Code

Azure infrastructure is managed using Terraform.

Terraform modules are organized under:

```text
infrastructure/terraform/modules/
```

Modules include:

```text
networking
aks
acr
keyvault
postgresql
redis
appgateway
```

Environment configuration is stored under:

```text
infrastructure/terraform/environments/dev/
```

Terraform state is stored remotely in Azure Storage.

The state container is private and uses Azure RBAC authentication.

Blob versioning is enabled to provide additional state protection.

---

## Application CI/CD Pipeline

Application deployments are automated using Azure DevOps.

```text
GitHub
   |
   v
Backend Tests
   |
   v
Repository / Dependency Security Scan
   |
   v
Docker Build
   |
   v
Push Image to ACR
   |
   v
Container Security Scan
   |
   v
Deploy to AKS
   |
   v
Smoke Test
```

Container images use unique pipeline Build ID tags.

This provides traceability between a pipeline execution and the deployed container version.

---

## Infrastructure Pipeline

Terraform infrastructure changes use a separate Azure DevOps pipeline.

```text
Terraform Validate
        |
        v
Terraform Security Scan
        |
        v
Terraform Plan
        |
        v
Manual Approval
        |
        v
Terraform Apply
```

The Apply stage consumes the Terraform plan artifact generated by the Plan stage.

Azure DevOps authenticates to Azure using Workload Identity Federation instead of stored client secrets.

---

## Security

Security controls include:

- Azure Workload Identity
- Azure DevOps Workload Identity Federation
- Azure RBAC
- Azure Key Vault secret management
- private PostgreSQL connectivity
- private Redis connectivity
- disabled ACR administrator credentials
- Kubernetes NetworkPolicies
- dedicated Kubernetes ServiceAccount
- container resource limits
- repository and dependency vulnerability scanning
- container image scanning
- Terraform Infrastructure-as-Code scanning
- pipeline blocking for HIGH and CRITICAL security findings

The Terraform development backend currently has a documented network security exception because Microsoft-hosted Azure DevOps agents require connectivity to the remote state storage endpoint.

Production hardening can move Terraform state access behind private networking with an appropriately networked agent.

---

## Monitoring and Alerting

Prometheus collects application metrics from the backend, scheduler, and workers.

Important metrics include:

```text
uptimehub_http_requests_total
uptimehub_http_request_duration_seconds
uptimehub_monitor_checks_total
uptimehub_monitor_check_failures_total
uptimehub_monitor_response_time_seconds
uptimehub_monitor_queue_size
```

Grafana provides dashboards for:

- API traffic
- request rate
- API latency
- monitor status
- monitoring queue behavior

Alertmanager processes Prometheus alerts and sends operational notifications by email.

Azure Monitor and Log Analytics provide additional Azure platform observability.

---

## Repository Structure

```text
uptimehub/
|
+-- application/
|   +-- backend/
|
+-- infrastructure/
|   +-- terraform/
|       +-- bootstrap/
|       +-- environments/
|       |   +-- dev/
|       +-- modules/
|           +-- networking/
|           +-- aks/
|           +-- acr/
|           +-- keyvault/
|           +-- postgresql/
|           +-- redis/
|           +-- appgateway/
|
+-- kubernetes/
|   +-- base/
|
+-- monitoring/
|   +-- prometheus/
|   +-- alerts/
|
+-- pipelines/
|   +-- azure-pipelines.yml
|   +-- terraform-pipeline.yml
|
+-- docs/
|   +-- architecture/
|   +-- operations/
|   +-- security/
|   +-- runbooks/
|
+-- compose.yaml
+-- README.md
```

---

## Local Development

The local environment can be started using Docker Compose:

```bash
docker compose up --build
```

The local stack includes the application backend, PostgreSQL, Redis, scheduler, workers, Prometheus, Grafana, and Alertmanager.

---

## Deployment Flow

A typical application change follows:

```text
Developer
    |
    v
GitHub
    |
    v
Azure DevOps
    |
    +--> Tests
    |
    +--> Security Scanning
    |
    +--> Docker Build
    |
    v
Azure Container Registry
    |
    v
Azure Kubernetes Service
    |
    v
Application Gateway
    |
    v
Users
```

Infrastructure changes follow:

```text
Terraform Code
      |
      v
Azure DevOps
      |
      v
Validate + Security
      |
      v
Terraform Plan
      |
      v
Approval
      |
      v
Terraform Apply
      |
      v
Azure Infrastructure
```

---

## Documentation

Additional documentation is available under `docs/`.

It includes:

- architecture documentation
- deployment procedures
- monitoring documentation
- security documentation
- incident response runbook
- rollback runbook
- troubleshooting guidance

---

## Current Environment

UptimeHub currently includes a complete development environment on Azure.

The development environment uses HTTP through Azure Application Gateway.

DNS and trusted TLS/HTTPS are intentionally deferred until a domain is introduced.

Additional production hardening can include private Terraform backend connectivity and production-specific availability and recovery requirements.