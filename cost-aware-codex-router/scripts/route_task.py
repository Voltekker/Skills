#!/usr/bin/env python3
"""Choose the cheapest reasonable model/reasoning pair for one work phase."""
import argparse


def route(phase, *, cross_subsystem=False, repeated_failure=False,
          critical_p0=False, independent_review=False):
    if independent_review or (critical_p0 and repeated_failure):
        return "sol", "high"
    if phase == "certification":
        return "terra", "high"
    if phase == "hard-defect" or cross_subsystem or repeated_failure:
        return "terra", "high"
    if phase in {"inventory", "audit"}:
        return "luna", "medium"
    return "terra", "medium"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--phase", choices=("inventory", "audit", "implementation",
                                             "verification", "certification",
                                             "hard-defect"), required=True)
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
    print(f"MODEL={model}")
    print(f"REASONING={reasoning}")


if __name__ == "__main__":
    main()
