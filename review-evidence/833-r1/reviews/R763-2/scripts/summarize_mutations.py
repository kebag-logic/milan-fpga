#!/usr/bin/env python3
"""usage: summarize_mutations.py <receipts/mutations dir> -- table of rc per mutant and control."""
import os, sys
d = sys.argv[1]
cs = ["owner_report", "owner_reparented", "owner_late_exit", "owner_stall",
      "owner_shell_window", "owner_survivor", "owner_vanishing"]
ms = sorted({f.rsplit(".", 2)[0] for f in os.listdir(d) if f.endswith(".rc")}, key=lambda m: (m != "none", m))
print("| mutant | " + " | ".join(c.replace("owner_", "") for c in cs) + " | red |")
print("|---|" + "---|" * len(cs) + "---:|")
reasons = []
for m in ms:
    row, red = [], 0
    for c in cs:
        rc = open(os.path.join(d, f"{m}.{c}.rc")).read().strip()
        if rc == "0":
            row.append("ok")
        else:
            red += 1
            row.append(f"RED({rc})")
            lines = [l for l in open(os.path.join(d, f"{m}.{c}.log")).read().splitlines() if l.strip()]
            reasons.append(f"{m} / {c}: {lines[-1][:170] if lines else ''}")
    print(f"| {m} | " + " | ".join(row) + f" | {red} |")
print()
print("\n".join(reasons))
