#!/usr/bin/env python3
"""Record the exact delta and independently inspect the notification inventory."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess

p = argparse.ArgumentParser(description=__doc__)
p.add_argument("repo", type=Path)
a = p.parse_args()
packet = Path(__file__).resolve().parents[1]
base = "ed340b9b85258194247334b85e62cf9c23d4d051"
baseline = "1411117e646023cb236de02e3acaf9bdfcef49e3"
def git(*args):
    return subprocess.check_output(["git", "-C", str(a.repo), *args]).decode()
changed = git("diff", "--name-only", baseline, "HEAD").splitlines()
assert changed == ["docs/architecture/09_verification.md"], changed
def non_delta_entries(revision):
    return [x for x in git("ls-tree", "-r", revision).splitlines()
            if x.split("\t", 1)[1] != changed[0]]
assert non_delta_entries(baseline) == non_delta_entries("HEAD")
text = (a.repo / changed[0]).read_text()
section = text.split("### 8.4 ", 1)[1].split("### 8.5 ", 1)[0]
rows = [l for l in section.splitlines() if l.startswith("|") and "`tb/aecp_notify`" in l]
assert len(rows) == 7
paths = ["hdl", "tb", "scripts", "syn", "docs/architecture/06_aecp_engine.md",
         "docs/architecture/07_memory_maps.md"]
unchanged = {}
for path in paths:
    before = git("rev-parse", f"{baseline}:{path}").strip()
    after = git("rev-parse", f"HEAD:{path}").strip()
    assert before == after
    unchanged[path] = {"baseline_object": before, "head_object": after}
rtl = "hdl/aecp/KL_aecp_notify.sv"
def count_two(s):
    return s.split("  if (N_IF_P > 1) begin : g_ca_turns\n", 1)[1].split("  end else begin : g_ca_own", 1)[0]
old = count_two(git("show", f"{base}:{rtl}"))
new = count_two(git("show", f"HEAD:{rtl}"))
assert new.replace("    assign cx_wait_w = '0;\n", "", 1) == old
record = {"head": git("rev-parse", "HEAD").strip(), "baseline": baseline,
          "changed_paths": changed, "unchanged_objects": unchanged,
          "identical_non_delta_blob_and_mode_entries": len(non_delta_entries("HEAD")),
          "notification_section_count": len(rows), "notification_rows": rows,
          "count_two_branch_equal_to_source_base_except_inactive_zero_tie": True,
          "required_submodule_gitlinks": [],
          "note": "The processor tree contains no gitlinks; parent integration is outside this clone."}
(packet / "receipts/scope-audit.json").write_text(json.dumps(record, indent=2) + "\n")
print("PASS: one documentation file changed; HDL/tests/scripts/records unchanged; seven notification rows")
