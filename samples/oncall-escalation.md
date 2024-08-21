# On-call Escalation Policy

## When to escalate

Page the secondary on-call if you have not found a root cause within 30 minutes,
if the incident affects more than 25% of users, or if the fix requires a database
schema change. For security incidents, escalate immediately to the Security on-call
regardless of impact.

## Escalation path

1. Primary on-call (responds within 5 minutes)
2. Secondary on-call (responds within 10 minutes)
3. Team lead (responds within 20 minutes)
4. Engineering manager, then VP Engineering

Escalation happens through PagerDuty. Never escalate by direct message alone; the
policy is that every page must exist in PagerDuty so the timeline is recorded.

## Severity definitions

- **SEV-1**: customer-facing outage, revenue impact, or data loss. Page immediately, 24/7.
- **SEV-2**: degraded service or a workaround exists. Page during business hours.
- **SEV-3**: minor issue with no meaningful customer impact. Handle via ticket.

## Communication

For SEV-1 and SEV-2, post an update in #incidents every 30 minutes until resolved.
The incident commander owns status updates and the customer-facing status page.
