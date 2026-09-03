# Cost-Aware Codex Router

A Codex skill for preventing expensive monolithic coding runs.

## Contents
- `SKILL.md` — routing, escalation and checkpoint policy.
- `scripts/estimate_task.py` — lightweight planning-time estimator.
- `scripts/route_task.py` — deterministic phase/model recommendation helper.
- `references/PLAYCE_PROFILE.md` — profile derived from the supplied PLAYCE realignment work order.
- `agents/openai.yaml` — UI metadata.

## Example estimator

```bash
python3 scripts/estimate_task.py \
  --docs 24 \
  --kloc 35 \
  --unit-groups 5 \
  --e2e-flows 10 \
  --complexity high \
  --model luna \
  --reasoning medium
```

Run the estimator again after Phase 1 with the actual number of remediation items.

For task-level model selection, run `python3 scripts/route_task.py --phase implementation`.
Apply its result only through a runtime that supports explicit model overrides.
