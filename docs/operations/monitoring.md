# UptimeHub Monitoring and Alerting

## Overview

UptimeHub uses Prometheus and Grafana for application observability.

Azure Monitor and Log Analytics provide Azure platform observability.

## Prometheus

Prometheus collects metrics from:

- backend
- scheduler
- workers

Important metrics include:

- uptimehub_http_requests_total
- uptimehub_http_request_duration_seconds
- uptimehub_monitor_checks_total
- uptimehub_monitor_check_failures_total
- uptimehub_monitor_response_time_seconds
- uptimehub_monitor_queue_size

## Grafana

Grafana dashboards provide visibility into:

- API request volume
- requests per second
- P95 API latency
- monitor checks by status
- queue behavior

## Alertmanager

Prometheus alert rules send alerts to Alertmanager.

Alertmanager delivers operational notifications by email.

Alert conditions include:

- application availability problems
- monitor check failures
- high API latency
- queue backlog
- unhealthy application components

## Kubernetes Troubleshooting

Useful commands:

`kubectl get pods -n uptimehub-dev`

`kubectl get deployments -n uptimehub-dev`

`kubectl get services -n uptimehub-dev`

`kubectl get ingress -n uptimehub-dev`

`kubectl get hpa -n uptimehub-dev`

`kubectl logs -n uptimehub-dev <pod-name>`

`kubectl describe pod -n uptimehub-dev <pod-name>`

`kubectl get events -n uptimehub-dev --sort-by=.metadata.creationTimestamp`

## Investigation Flow

Alert -> Grafana/Prometheus -> Kubernetes -> Logs -> Dependencies ->
Azure platform -> Mitigation -> Incident documentation.
