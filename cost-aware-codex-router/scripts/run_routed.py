#!/usr/bin/env python3
"""Run one Codex phase in a fresh process with the routed model."""
import argparse
import os
import shutil
import subprocess
import sys
from pathlib import Path

from route_task import route


MODEL_IDS = {
    "luna": "gpt-5.6-luna",
    "terra": "gpt-5.6-terra",
    "sol": "gpt-5.6-sol",
}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("inventory", "audit", "implementation",
                                             "verification", "certification",
                                             "hard-defect"), required=True)
    parser.add_argument("--cd", type=Path, default=Path.cwd())
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--cross-subsystem", action="store_true")
    parser.add_argument("--repeated-failure", action="store_true")
    parser.add_argument("--critical-p0", action="store_true")
    parser.add_argument("--independent-review", action="store_true")
    args = parser.parse_args()

    model, reasoning = route(
        args.phase,
        cross_subsystem=args.cross_subsystem,
        repeated_failure=args.repeated_failure,
        critical_p0=args.critical_p0,
        independent_review=args.independent_review,
    )
    model_id = os.environ.get(f"COST_ROUTER_{model.upper()}_MODEL", MODEL_IDS[model])
    command = ["codex", "exec", "--model", model_id, "--cd", str(args.cd)]
    print(f"ROUTED_MODEL={model_id}")
    print(f"ROUTED_REASONING={reasoning}")
    if args.dry_run:
        print("COMMAND=" + " ".join(command) + " -")
        return

    if shutil.which("codex") is None:
        raise SystemExit("codex CLI not found on PATH")
    raise SystemExit(subprocess.run(command + ["-"], cwd=args.cd).returncode)


if __name__ == "__main__":
    main()
