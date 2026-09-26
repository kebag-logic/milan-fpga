#!/usr/bin/env python3
"""Map the baseline page's refusal categories to the self-test's refusal arms.

Usage: python3 category_map.py <clone>
Runs <clone>/syn/ooc/pp_baseline.py --selftest, classifies every refusal arm
the source exercises, and reports which page categories have arms and which
arms fall under no named category. Read-only: nothing in <clone> is written
except what the self-test itself creates and removes in a temporary directory.
"""
import re
import subprocess
import sys
from pathlib import Path

clone = Path(sys.argv[1]).resolve()
source = (clone / "syn/ooc/pp_baseline.py").read_text()
page = (clone / "docs/findings/PP_SHADOW_BASELINE.md").read_text().splitlines()
run = subprocess.run([sys.executable, "-B", str(clone / "syn/ooc/pp_baseline.py"), "--selftest"],
                     capture_output=True, text=True, timeout=300)
print(f"selftest rc={run.returncode}")
out = run.stdout
labels = re.findall(r"^baseline inventory refusal: (.+) PASS$", out, re.M)

def inventory_category(label: str) -> str:
    if label in ("missing generated ROM", "unlisted readmemh"):
        return "inventory"
    if label.endswith((" duplicate", " missing")) and label.split()[0].endswith("_HEX_P"):
        return "binding"
    if label.endswith((" short", " long", " narrow", " wide")) or label == "nonempty SRAM":
        return "geometry"
    return "declaration"  # package read or depth/width declaration duplicate/missing

counts: dict[str, int] = {}
for label in labels:
    counts[inventory_category(label)] = counts.get(inventory_category(label), 0) + 1
# Endpoint self-test arms, classified from the source text of export_endpoint_selftest.
endpoint = source[source.index("def export_endpoint_selftest"):source.index("def export_selftest")]
counts["endpoint"] = endpoint.count('expect_refusal("integrated scripts must run') + \
    endpoint.count('expect_refusal("attribution requires an integrated build")')
counts["template (single synthesis command)"] = 2 if 'expected exactly one integrated synthesis command' in endpoint else 0
counts["pathname"] = len(re.findall(r"'bad[{}\"]path'", endpoint))
counts["CLI containment"] = len(re.findall(r'"--(synthesis|attribution)-only"', endpoint)) + \
    (1 if "in-repository output accepted" in source else 0)
for key in sorted(counts):
    print(f"arm category {key}: {counts[key]}")
print("inventory labels:", len(labels))
for line in out.splitlines():
    if not line.startswith("baseline inventory refusal:") and not line.startswith("/"):
        print("selftest:", line)
claim = [(n + 1, l) for n, l in enumerate(page) if "refusal" in l or "mutant" in l]
for n, l in claim:
    print(f"page:{n}: {l}")
named = ["inventory", "geometry", "binding", "declaration", "endpoint", "pathname", "CLI containment"]
text = " ".join(l for _, l in claim)
for name in named:
    print(f"named on page and exercised: {name}: page={name in text} arms={counts.get(name, 0)}")
print("exercised but not named on page: template (single synthesis command):",
      counts["template (single synthesis command)"])
