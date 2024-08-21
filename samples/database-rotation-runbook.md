# Database Credential Rotation Runbook

This runbook covers rotation of the PostgreSQL credentials used by the `billing-api`
service. Rotation is performed quarterly, and immediately after any suspected leak.
The whole procedure takes about 15 minutes and requires no downtime.

## Prerequisites

You need access to the `platform-prod` vault namespace and permission to run
`kubectl rollout restart` on the `billing` namespace. Confirm that the replica set
is healthy (`kubectl get pods -n billing`) before you begin.

## Steps

1. Generate a new password in the vault: `vault write -f database/creds/billing-ro`.
   The vault returns a lease ID; record it in the rotation ticket.
2. Update the Kubernetes secret `billing-db` with the new username and password:
   `kubectl create secret generic billing-db --from-env-file=.env --dry-run=client -o yaml | kubectl apply -f -`.
3. Restart the deployment so pods pick up the new secret:
   `kubectl rollout restart deployment/billing-api -n billing`.
4. Watch the rollout with `kubectl rollout status deployment/billing-api -n billing`.
   Each pod should become ready within 60 seconds.
5. After all pods are healthy, revoke the old credential lease in the vault using
   `vault lease revoke <old-lease-id>`.

## Verification

Check the application log for `auth_failure` entries for 10 minutes after rotation.
If any appear, re-apply the previous secret and open an incident. The old credential
stays valid until step 5, so rollback is always possible during the window.

## Rollback

Apply the previous secret version with `kubectl rollout undo deployment/billing-api -n billing`,
then restore the old credential lease in the vault and close the rotation ticket with
a note explaining the failure.
