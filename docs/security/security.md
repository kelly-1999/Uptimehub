# UptimeHub Security

## Identity

UptimeHub uses Azure identities instead of embedded Azure credentials where
supported.

Azure DevOps authenticates to Azure using Workload Identity Federation.

AKS application workloads use Azure Workload Identity.

## Secrets

Application secrets are stored in Azure Key Vault.

Important secrets include:

- database connection URL
- Redis connection URL

The Kubernetes Secrets Store CSI Driver retrieves secrets from Key Vault.

Secrets must not be committed to Git.

Local `.env` files are excluded from source control.

## Container Registry

Azure Container Registry administrator credentials are disabled.

AKS retrieves container images using Azure identity and the AcrPull role.

## Network Security

PostgreSQL is not publicly exposed.

Azure Managed Redis is not publicly exposed.

Private networking and Private DNS are used for backend data services.

Kubernetes NetworkPolicies restrict traffic where appropriate.

## Kubernetes Security

Application workloads use:

- resource requests and limits
- startup, readiness and liveness probes
- dedicated ServiceAccount
- Azure Workload Identity
- NetworkPolicy
- PodDisruptionBudget
- Horizontal Pod Autoscaler

## CI/CD Security

Automated security controls include:

- dependency and repository scanning
- Terraform Infrastructure-as-Code scanning
- container image scanning

HIGH and CRITICAL security findings can block the pipeline.

## Terraform State

Terraform state is stored in a private Azure Storage container.

Controls include:

- Azure RBAC
- TLS 1.2 minimum
- blob versioning
- private container access

The development environment currently permits the storage public endpoint
because Microsoft-hosted Azure DevOps agents require connectivity to the
Terraform backend.

This is documented as a development security exception.

Production hardening should use private backend connectivity with an
appropriately networked build agent.

## Security Principles

UptimeHub follows:

- least privilege
- no secrets in source control
- identity-based authentication
- private data services
- automated security scanning
- encrypted connections
- controlled infrastructure deployment
