# UptimeHub Incident Response Runbook

## Purpose

This runbook describes how to investigate UptimeHub service incidents.

## 1. Identify the Problem

Determine:

- affected component
- start time
- environment
- user impact
- whether the issue is ongoing

## 2. Check Kubernetes

Check pods, deployments, autoscaling and Kubernetes events.

Look for:

- CrashLoopBackOff
- ImagePullBackOff
- failed health probes
- pending pods
- unexpected restarts

## 3. Check Logs

Inspect application logs for the affected workload.

For restarted containers, inspect the previous container logs when available.

## 4. Check Dependencies

Verify connectivity and health for:

- PostgreSQL
- Redis
- Azure Key Vault
- Azure Container Registry

## 5. Check Monitoring

Review Prometheus and Grafana.

Investigate:

- request rate
- latency
- errors
- failed monitor checks
- Redis queue size

## 6. Check Recent Deployments

Review recent Azure DevOps application and infrastructure pipeline runs.

Determine whether the incident started after a deployment.

## 7. Mitigate

Possible mitigation actions include:

- rollback an application deployment
- restart a failed workload
- correct configuration
- restore dependency connectivity
- scale capacity
- correct infrastructure through Terraform

Avoid undocumented infrastructure changes.

## 8. Confirm Recovery

Confirm that workloads are healthy, monitoring has recovered, and the alert
condition has cleared.

## 9. Document the Incident

Record:

- timeline
- root cause
- impact
- mitigation
- corrective action
