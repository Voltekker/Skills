# PLAYCE routing profile

Use this profile when the repository/task is PLAYCE or a work order with the same structure.

## Authoritative behavior
The work order states that package documents are authoritative over existing code/tests/older reports. Codex must not invent missing product decisions. Ambiguity blocks only the affected point.

## Mandatory work characteristics
The supplied work order requires:
- reading all package documents before modifications;
- requirement-by-requirement audit;
- PASS / FAIL / PARTIAL / NOT VERIFIED / BLOCKED classification;
- gap analysis;
- dependency/risk remediation plan;
- implementation against the existing app rather than unnecessary rewrite;
- test updates;
- real backend/deploy verification when applicable;
- end-to-end verification before closure;
- intermediate TONE_CONTENT_INDEX delivery;
- final evidence for every P0 requirement.

This combination must be treated as a multi-phase order by the router.

## Recommended checkpoint sequence
1. Inventory + time/cost budget.
2. Requirement index + audit matrix, no code changes.
3. P0 remediation batches.
4. TONE_CONTENT_INDEX as soon as UI/copy surfaces stabilize.
5. E2E verification on real applicable systems.
6. Final P0 certification.

## Cost traps to avoid
- Reopening every authoritative document for every requirement.
- Treating existing tests as sufficient evidence where E2E behavior is required.
- Running the entire browser suite after every local change.
- Using a flagship/high-reasoning model for inventory and bulk PASS/FAIL bookkeeping.
- Keeping the escalated model after the hard defect that justified escalation has been solved.
