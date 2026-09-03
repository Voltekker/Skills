#!/usr/bin/env python3
"""Run a read-only, multi-phase Codex validation with automatic model routing."""
import argparse
import os
import shutil
import subprocess
import tempfile
from pathlib import Path

from route_task import route


PHASES = (
    ("inventory", "Inspect the repository and supplied instructions. Build the Task Budget Card and handoff."),
    ("audit", "Audit requirements against implementation. Produce PASS/FAIL/PARTIAL/NOT VERIFIED/BLOCKED evidence and P0/P1/P2 gaps."),
    ("security", "Audit auth, authorization, RLS, input validation, data integrity, idempotency, secrets, and mock/analytics boundaries."),
    ("verification", "Run the smallest relevant tests and verify required mobile, desktop, backend, and deployment flows. Do not modify files."),
    ("certification", "Independently certify P0 requirements, unresolved risks, evidence, and blockers. Do not modify files."),
)
MODEL_IDS = {"luna": "gpt-5.6-luna", "terra": "gpt-5.6-terra", "sol": "gpt-5.6-sol"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--instructions", type=Path, required=True)
    parser.add_argument("--cd", type=Path, default=Path.cwd())
    parser.add_argument("--artifacts-dir", type=Path)
    parser.add_argument("--independent-review", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    if not args.instructions.is_file():
        parser.error(f"instructions file not found: {args.instructions}")
    if shutil.which("codex") is None and not args.dry_run:
        parser.error("codex CLI not found on PATH")

    artifacts = args.artifacts_dir or Path(tempfile.mkdtemp(prefix="codex-router-"))
    artifacts.mkdir(parents=True, exist_ok=True)
    base = args.instructions.read_text()
    previous = ""
    print(f"ARTIFACTS={artifacts}")
    for phase, objective in PHASES:
        model, reasoning = route(phase, independent_review=args.independent_review and phase == "certification")
        model_id = os.environ.get(f"COST_ROUTER_{model.upper()}_MODEL", MODEL_IDS[model])
        command = ["codex", "exec", "--ephemeral", "--model", model_id,
                   "-c", f'model_reasoning_effort="{reasoning}"', "--cd", str(args.cd), "-"]
        prompt = f"""{base}

ROUTER CONTROL: You are running phase {phase}. Do not modify files, databases, deployments, or configuration.
Objective: {objective}
Return the required checkpoint fields from the skill. Write a compact handoff suitable for the next phase.

Previous phase handoff:
{previous}
"""
        print(f"PHASE={phase} MODEL={model_id} REASONING={reasoning}")
        if args.dry_run:
            print("COMMAND=" + " ".join(command))
            continue
        result = subprocess.run(command, input=prompt, text=True, capture_output=True, cwd=args.cd)
        output = result.stdout + result.stderr
        (artifacts / f"{phase}.md").write_text(output)
        previous = output[-12000:]
        if result.returncode:
            print(f"STOPPED={phase} EXIT={result.returncode}")
            raise SystemExit(result.returncode)
    print("STATUS=complete" if not args.dry_run else "STATUS=dry-run")


if __name__ == "__main__":
    main()
