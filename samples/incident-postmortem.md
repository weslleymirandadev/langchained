# Incident Postmortem: 2026-02-11 Search Outage

**Severity:** SEV-2
**Duration:** 47 minutes (14:03 - 14:50 UTC)
**Impact:** Search returned HTTP 503 for ~12% of requests; document uploads were unaffected.

## Summary

A routine index compaction job ran during peak traffic and saturated the disk IOPS
on the search nodes. Queries timed out and the load balancer began shedding traffic.

## Timeline

- 14:03 - Pager fires for elevated 5xx rate on the search service.
- 14:07 - On-call confirms 503s and sees disk queue depth above 200 on nodes s-3, s-4.
- 14:12 - Compaction job identified as the cause; job is paused.
- 14:21 - Query latency recovers, but one node remains unhealthy.
- 14:33 - Unhealthy node replaced by autoscaling after failing health checks.
- 14:50 - Error rate back to baseline; incident marked resolved.

## Root cause

The compaction job had no IOPS budget and was configured to run at a fixed time
rather than in a low-traffic window. It ran concurrently across all shards, which
multiplied disk pressure beyond what the node pool could absorb.

## What went well

Alerting fired within 3 minutes and the runbook correctly identified the compaction job.

## What went wrong

The compaction job is not visible in the standard dashboard, so the first responder
had to query the database directly. Also, the autoscaler took 12 minutes to replace a node.

## Action items

1. Move compaction to 02:00 UTC and limit it to two shards at a time. Owner: Search team.
2. Add compaction progress and IOPS to the search dashboard. Owner: Observability.
3. Tune autoscaler to replace unhealthy nodes within 5 minutes. Owner: Platform.
4. Add an IOPS guardrail that pauses compaction above 70% utilisation. Owner: Search team.
