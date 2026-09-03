#!/usr/bin/env python3
"""Planning-only estimator for Codex engineering work.

Produces a range intended for task splitting/model routing, not a delivery promise.
No network access or external packages required.
"""
import argparse

MODEL = {"luna": 0.82, "terra": 1.00, "sol": 1.12}
REASON = {"low": 0.88, "medium": 1.00, "high": 1.22, "max": 1.55}
COMPLEXITY = {"low": 0.85, "medium": 1.00, "high": 1.35, "extreme": 1.75}


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--docs", type=int, default=0)
    p.add_argument("--kloc", type=float, default=0)
    p.add_argument("--unit-groups", type=int, default=0)
    p.add_argument("--e2e-flows", type=int, default=0)
    p.add_argument("--remediation-items", type=int, default=0)
    p.add_argument("--complexity", choices=COMPLEXITY, default="medium")
    p.add_argument("--model", choices=MODEL, default="terra")
    p.add_argument("--reasoning", choices=REASON, default="medium")
    a = p.parse_args()

    # Deliberately conservative planning weights in active-work minutes.
    base = 2.0
    base += a.docs * 1.25
    base += min(a.kloc, 80) * 0.22
    base += max(0, a.kloc - 80) * 0.10
    base += a.unit_groups * 1.8
    base += a.e2e_flows * 3.5
    base += a.remediation_items * 4.0

    factor = COMPLEXITY[a.complexity] * MODEL[a.model] * REASON[a.reasoning]
    center = base * factor

    # Wider uncertainty for remediation/E2E and high complexity.
    uncertainty = 0.30
    uncertainty += min(a.e2e_flows, 10) * 0.018
    uncertainty += min(a.remediation_items, 15) * 0.012
    if a.complexity == "high":
        uncertainty += 0.12
    elif a.complexity == "extreme":
        uncertainty += 0.25
    uncertainty = min(0.75, uncertainty)

    low = max(3, center * (1 - uncertainty))
    high = center * (1 + uncertainty)

    reasons = []
    if high > 45:
        reasons.append("upper estimate exceeds 45 minutes")
    if a.docs > 12:
        reasons.append("more than 12 authoritative documents")
    if a.e2e_flows > 8:
        reasons.append("more than 8 E2E flows")
    if a.remediation_items > 10:
        reasons.append("large remediation set")

    print(f"Planning estimate: {low:.0f}-{high:.0f} min (center {center:.0f} min)")
    print(f"Model/reasoning: {a.model}/{a.reasoning}")
    print(f"Complexity factor: {factor:.2f}; uncertainty: ±{uncertainty*100:.0f}%")
    if reasons:
        print("SPLIT RECOMMENDED: yes")
        for r in reasons:
            print(f"- {r}")
    else:
        print("SPLIT RECOMMENDED: no")
    print("Note: planning range only; recalibrate after inventory/audit evidence.")

if __name__ == "__main__":
    main()
