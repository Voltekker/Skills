---
name: cost-aware-codex-router
description: Use before or during substantial Codex software-engineering tasks to control model cost, estimate execution time, split long-horizon work into bounded phases, prevent unnecessary rereading/retesting, and recommend escalation from Luna to Terra to Sol only when justified. Especially useful for repository-wide audits, spec-to-implementation verification, remediation plans, browser/E2E verification, migrations, and work orders that combine reading, implementation, testing, and certification.
---

# Cost-Aware Codex Router

Use this skill as a governance layer for substantial coding work. Its goal is to preserve correctness while avoiding expensive monolithic runs.

## Core principle

Use the cheapest model reasonably capable of the **current phase**, not the hardest model that could complete the entire project.

Do not treat model choice as a speed-only decision. Lower-cost models may be less reliable on ambiguous, cross-cutting, highly coupled reasoning. Escalate only when observed task complexity justifies it.

## Important runtime limitation

This skill may recommend a model/reasoning level and may structure work for escalation. Do not claim that the skill itself has switched the current Codex session's model unless the runtime exposes and successfully executes an explicit model-switch mechanism.

If automatic switching is unavailable:
1. Continue with the current model only when it is appropriate for the phase.
2. At an escalation boundary, state the recommended model/reasoning level in one short line.
3. Preserve a compact handoff artifact so the next phase does not need to reread the full history.

When the runtime supports per-task model selection, run `scripts/route_task.py`
at each phase boundary and apply its `MODEL` and `REASONING` result to the next
task. Do not switch a parent session by implication; only use an explicit
runtime override that reports success.

For Codex CLI users, use `scripts/run_routed.py --phase <phase>`. It starts a
fresh `codex exec --model ...` process, which is the supported way to apply the
choice. Pass the compact handoff artifact or phase prompt through stdin. Use
`--dry-run` to inspect the selected model without starting Codex.

If the user includes the standalone token `RUN_ROUTER` at the beginning or end
of a complex validation or realignment prompt, treat it as an explicit request
to run `scripts/run_router.py --mode realignment`. Do not answer the work order
directly in the coordinator session: collect the user prompt and attachment
paths into a temporary instructions file, invoke the orchestrator through the
available runtime, and return its phase/checkpoint results. Use
`RUN_ROUTER_AUDIT` for read-only validation with `--mode audit`. Carry each
phase output into the next one. These are skill trigger conventions, not native
UI commands.

## Default routing policy

### Luna + medium
Use for bounded, mostly deterministic or high-volume work:
- repository inventory;
- documentation indexing and requirement extraction;
- locating code paths;
- build, lint, typecheck and routine unit tests;
- mechanical edits;
- repetitive PASS / FAIL classification when evidence is explicit;
- generating matrices from already-understood evidence;
- targeted regression tests after local changes.

### Terra + medium
Use as the default implementation engine for:
- normal feature implementation;
- ordinary debugging;
- spec-to-code comparison requiring judgment;
- browser verification of well-defined flows;
- backend/frontend integration work;
- E2E remediation with clear expected behavior.

### Terra + high
Escalate when at least one is true:
- root cause spans 3 or more subsystems;
- concurrency, realtime, state synchronization, auth, data consistency, or lifecycle behavior is involved;
- two reasonable fixes have materially different side effects;
- repeated local fixes fail to resolve the issue;
- requirements are individually clear but their interaction is difficult to reason about.

### Sol + high
Reserve for demonstrated hard cases:
- Terra failed twice with materially different approaches;
- architecture-level reasoning is required before changing code;
- multiple specifications interact in a way that creates non-obvious global constraints;
- a critical P0 defect remains unexplained after targeted instrumentation/testing;
- final high-stakes certification needs an independent deep review.

### Avoid by default
- Sol for bulk reading, indexing, linting, routine tests, repetitive remediation or ordinary browser clicking.
- Maximum/xhigh reasoning for long autonomous runs unless explicitly justified.
- Re-running broad E2E suites after every small edit.
- Re-reading the full specification set when a requirement index already exists.

## Phase gate: never start large work blindly

Before substantial work, create a **Task Budget Card** containing:

- Scope summary.
- Files/docs likely to be read.
- Approximate repository surface.
- Test surface.
- Browser/E2E surface.
- Coupling/ambiguity risk.
- Recommended model + reasoning for the first phase.
- Estimated elapsed-time range for the first phase.
- Estimated elapsed-time range for the full work order, clearly marked as provisional.
- Stop condition for the phase.

Do not spend a long run merely producing this card. Use quick repository/document inventory commands and existing metadata.

## Time estimation protocol

Time estimates are planning ranges, not promises. Re-estimate after Phase 1 with observed evidence.

If available, run `scripts/estimate_task.py` with observed counts. Otherwise apply the same logic manually.

Use `scripts/route_task.py` for the model/reasoning choice when the runtime
exposes task-level overrides. Its output is a recommendation, not proof that a
switch occurred.

### Inputs
Estimate these values:
- `docs`: authoritative documents that must be materially read;
- `kloc`: approximate application source size in thousands of lines, excluding dependencies/build output;
- `unit_groups`: distinct test groups/commands likely to run;
- `e2e_flows`: user-visible flows that need real/browser verification;
- `remediation_items`: known FAIL/PARTIAL items requiring code changes; use 0 before audit if unknown;
- `complexity`: low / medium / high / extreme;
- `model`: luna / terra / sol;
- `reasoning`: low / medium / high / max.

### Interpretation
The estimator returns:
- a base active-work estimate;
- a lower and upper range;
- a risk multiplier;
- a recommendation to split the work if the upper range is too large.

Do not convert the estimate into a promise to deliver later. It exists only to decide scope, model and checkpoints for the current execution.

### Mandatory split thresholds
Split the work into checkpoints if any of the following is true:
- estimated upper bound > 45 minutes;
- more than 12 authoritative documents must be read;
- more than 8 E2E flows require browser verification;
- audit + implementation + E2E + final certification are all requested in one order;
- the work spans frontend + backend + persistence/realtime/auth plus product specification;
- context is likely to require repeated full-spec rereads.

## Standard phase architecture

For repository-wide realignment/audit work, prefer:

### Phase 0 — Budget + inventory
- Inspect repository shape and authoritative sources.
- Produce Task Budget Card.
- Do not modify code.
- Stop once routing and phase boundaries are established.

### Phase 1 — Specification audit
Recommended default: Luna/medium, or Terra/medium if requirements are highly interdependent.
- Read/index authoritative sources once.
- Build a stable requirement index with source anchors.
- Audit implementation against requirements.
- Produce PASS / FAIL / PARTIAL / NOT VERIFIED / BLOCKED evidence.
- Produce gap list.
- Do not remediate unless explicitly required to continue immediately.
- Persist a compact audit artifact.

### Phase 2 — Remediation
Recommended default: Terra/medium.
- Work only from FAIL/PARTIAL items and their targeted source references.
- Order work by dependency and risk.
- Make minimal compatible changes.
- Run targeted tests after each logical change.
- Escalate only individual hard defects, not the entire phase.

### Phase 3 — E2E / real-system verification
Recommended default: Terra/medium or high.
- Verify defined user-visible flows on the real applicable backend/deploy.
- Capture concise evidence.
- Fix only reproducible defects.
- Re-run affected flows, not every flow after every change.

### Phase 4 — Certification
Recommended default: Terra/high; use Sol/high only when risk justifies an independent deep review.
- Recheck P0 requirements against actual evidence.
- Identify anything still NOT VERIFIED/BLOCKED.
- Never upgrade status to PASS from code presence alone when end-to-end evidence is required.

## Context-cost controls

1. **Read once, index once.** Create a compact requirement map and use precise references thereafter.
2. **Bound tool output.** Prefer filtered logs, targeted test files, targeted grep/search and concise diagnostics.
3. **Do not dump huge files into context** when a section/range is sufficient.
4. **Test locally first.** Run the smallest relevant test before a full suite.
5. **Browser selectively.** Verify flows required by acceptance criteria; avoid exploratory repetition without a hypothesis.
6. **Checkpoint after meaningful batches.** Summarize changed files, evidence, remaining gaps and next model recommendation.
7. **Avoid recursive audit loops.** A requirement already supported by unchanged evidence need not be re-audited after unrelated edits.
8. **Preserve authoritative wording.** Do not invent missing product requirements to save time.

## Escalation protocol

Escalation must be evidence-based. Before recommending a more expensive model, write:

`ESCALATION: <current> -> <recommended> | reason: <one concrete observed difficulty>`

Valid reasons include:
- repeated failed fixes;
- cross-subsystem causal ambiguity;
- conflicting constraints requiring architectural judgment;
- critical unexplained defect;
- final independent certification.

Invalid reasons include:
- repository is large;
- many files need reading;
- many tests need running;
- task is tedious;
- wanting maximum confidence without a concrete hard reasoning problem.

## De-escalation protocol

After a hard issue is resolved, return bulk work to the cheaper appropriate tier. Do not keep Sol active for subsequent routine edits/testing merely because one issue required it.

## PLAYCE-style work orders

When an order requires all of the following together:
- full authoritative-document reading;
- requirement-by-requirement audit;
- gap analysis;
- remediation;
- test updates;
- real backend/deploy verification;
- end-to-end certification;

it is automatically a multi-phase order. Do not execute it as one uninterrupted pass.

Preserve explicit product-owner gates. If the specification says to stop only on the ambiguous point and ask, isolate that point; continue independent non-blocked work when possible.

For a PLAYCE-like order, default routing is:
- Phase 0: Luna/medium
- Phase 1: Luna/medium, Terra/medium if cross-requirement interpretation becomes material
- Phase 2: Terra/medium
- hard individual defect: Terra/high -> Sol/high only if needed
- Phase 3: Terra/medium/high
- Phase 4: Terra/high, optionally Sol/high for independent P0 review

## Required output at every phase boundary

Return a compact checkpoint:

```text
PHASE: <name>
STATUS: complete | partial | blocked
MODEL RECOMMENDATION NEXT: <model>/<reasoning>
ELAPSED WORK OBSERVED: <only if runtime exposes it; otherwise omit>
RE-ESTIMATED NEXT PHASE: <range>
RE-ESTIMATED REMAINING WORK: <range>
COMPLETED: <short list>
OPEN: <short list>
BLOCKERS: <short list or none>
HANDOFF ARTIFACT: <path if created>
```

Never fabricate elapsed runtime. If runtime duration is unavailable, omit it.

## Definition of success

This skill succeeds when:
- expensive reasoning is applied only where it improves expected correctness;
- long-horizon work is split before context grows unnecessarily;
- the agent produces usable intermediate evidence rather than one giant final pass;
- model escalation is justified by observed difficulty;
- task-duration estimates are ranges and are recalibrated from actual audit evidence;
- functional correctness and authoritative specifications are not sacrificed merely to reduce cost.
