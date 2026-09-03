# Cost-Aware Codex Router

A Codex skill for preventing expensive monolithic coding runs.

## Contents
- `SKILL.md` — routing, escalation and checkpoint policy.
- `scripts/estimate_task.py` — lightweight planning-time estimator.
- `scripts/route_task.py` — deterministic phase/model recommendation helper.
- `scripts/run_routed.py` — launches a fresh Codex CLI phase with the selected model.
- `scripts/run_router.py` — runs validation or full realignment with automatic phase switching.
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

To apply the choice with Codex CLI:

```bash
python3 scripts/run_routed.py --phase implementation --cd /path/to/repo < phase-prompt.md
```

The launcher starts a new process with `--model`; it does not mutate an already-running session.

For a complete validation workflow:

```bash
python3 scripts/run_router.py \
  --instructions istruzioni-playce.md \
  --cd /path/to/PLAYCE
```

For validation plus implementation of the useful, unambiguous changes:

```bash
python3 scripts/run_router.py \
  --mode realignment \
  --instructions istruzioni-playce.md \
  --cd /path/to/PLAYCE
```

Realignment permits code and test changes only in remediation/verification;
deployment, push, and secret changes remain out of scope.

The literal `/run_router` at the top or bottom of a prompt is the skill's
trigger convention. Native UI slash-command registration is not provided by
the Codex Skills format.
