# UptimeHub Rollback Runbook

## Purpose

This runbook describes recovery from an unsuccessful UptimeHub deployment.

## Application Rollback

Inspect backend deployment history:

`kubectl rollout history deployment/uptimehub-backend -n uptimehub-dev`

Rollback:

`kubectl rollout undo deployment/uptimehub-backend -n uptimehub-dev`

Check rollout:

`kubectl rollout status deployment/uptimehub-backend -n uptimehub-dev --timeout=300s`

The same process can be used for scheduler and worker Deployments when
appropriate.

## Container Version Rollback

Every pipeline build produces a uniquely tagged image in Azure Container
Registry.

A previous known-good image can therefore be redeployed.

Application image changes should normally go through the deployment pipeline
to maintain traceability.

## Database Considerations

Application rollback does not automatically reverse an Alembic database
migration.

Schema changes should therefore maintain backward compatibility where
possible.

Database recovery planning should account for migrations and backups.

## Infrastructure Rollback

Do not normally rollback Terraform-managed infrastructure by manually changing
Azure resources.

Instead:

1. Revert the Terraform source change.
2. Run Terraform Validate.
3. Run the security scan.
4. Generate a new Terraform Plan.
5. Review the plan.
6. Approve Terraform Apply.

This keeps Azure infrastructure aligned with Terraform state and source
control.
